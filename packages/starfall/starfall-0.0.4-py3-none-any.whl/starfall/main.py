#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: alex
@date:   2022/05/18
"""

import logging.config
import threading
import requests
import json
from threading import Timer
import socket
import time
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from starfall.helper import LogParam, TriggerParam, response_ok, SUCCESS_RESP, response_err, read_log_line
import executor
from waitress import serve
import os
import configparser
import json

logger = None

port = 9002
app_name = 'starfall'
job_admin_uri = None
job_admin_access_token = None
runtime_log_path = None


app = Flask(__name__)


def init(proj_path: str):
    # 初始化
    # 从环境变量获取日志路径配置
    runtime_log_path = os.environ.get(
        'LOG_PATH', os.path.join(proj_path, 'log'))
    # 自动创建日志目录
    if os.path.exists(runtime_log_path) == False:
        os.makedirs(runtime_log_path)
    # 解析日志配置
    log_config = os.path.join(proj_path, 'logging.json')
    if os.path.exists(log_config):
        with open(log_config) as f:
            log_config_obj = json.load(f)
        logging.config.dictConfig(log_config_obj)

    logger = logging.getLogger('main.base')
    # 解析配置
    parser = configparser.ConfigParser()
    parser.read(os.path.join(proj_path, 'conf.ini'))
    # 端口号
    port = parser.getint('Executor', 'PORT')
    # 注册应用name
    app_name = parser.get('Executor', 'NAME')
    job_admin_uri = parser.get('Executor', 'ADMIN_URI')
    job_admin_access_token = parser.get('Executor', 'ACCESS_TOKEN')

    print(f'''
      -----------------------------
      port: {port}
      name: {app_name}
      admin_uri: {job_admin_uri}
      access_token: {job_admin_access_token}
      -----------------------------
      ''')


# start serve
def start_serve():
    if job_admin_uri is None:
        raise Exception(f'配置参数`ADMIN_URI`不能为空')
    if app_name is None:
        raise Exception(f'配置参数`APP_NAME`不能为空')
    serve(app, host='0.0.0.0', port=port)


def resolve_request_to(class_):
    """转换请求json对象为实体类
    Args:
        class_ (_type_): 实体类
    """
    def wrap(f):
        def decorator(*args):
            obj = class_(**request.get_json())
            return f(obj)
        return decorator
    return wrap


def resolve_request_to_log(class_):
    """转换请求json对象为LogParams
    Args:
        class_ (_type_): 实体类
    """
    def wrap(f):
        def decoratorOfLog(*args):
            obj = class_(**request.get_json())
            return f(obj)
        return decoratorOfLog
    return wrap


@app.after_request
def af_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTION'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route("/")
def index():
    """返回相关描述信息
    """
    return response_ok({
        'app_name': app_name,
        'job_admin_uri': job_admin_uri,
        'access_token': job_admin_access_token,
        'proj_root_dir': PROJ_ROOT
    })


@app.route("/beat")
def beat():
    """执行器心跳检测
    """
    logger.info('beating...')
    return SUCCESS_RESP


@app.route("/idleBeat", methods=['POST'])
def idle_beat():
    """执行器空闲检测
    """
    # if request.is_json is False:
    #     return jsonify({'status': -1, 'msg': 'make sure the request Content-Type:application/json'})
    req_data = request.get_json()
    if 'jobId' in req_data:
        try:
            jobId = request.get_json()['jobId']
            return executor.idle_beat(jobId=jobId)
        except Exception as e:
            logger.exception(e)
            return jsonify({'code': 500, 'msg': str(e)})
    else:
        return response_err('`jobId` 参数不能为空')


@app.route("/run", methods=['POST'])
@resolve_request_to(TriggerParam)
def run_job(triggerParam):
    """运行任务
    Args:
        triggerParam (_type_): 运行参数实例
    """
    #  执行一个job
    return executor.run(triggerParam)


@app.route("/log", methods=['POST'])
@resolve_request_to_log(LogParam)
def get_log(logParam):
    """获取日志信息 TODO
    """
    print(str(logParam))
    return read_log_line(logParam)


@app.route("/kill", methods=['POST'])
def kill():
    """远程中止任务
    """
    req_data = request.get_json()
    if 'jobId' in req_data:
        try:
            jobId = request.get_json()['jobId']
            executor.kill(jobId=int(jobId))
        except Exception as e:
            logger.exception(e)
            return jsonify({'status': -1, 'msg': str(e)})
    else:
        return response_err('`jobId` 参数不能为空')

    return SUCCESS_RESP


# region -----------------core methods----------------------

address = ''
req_headers = {}
timer = None


def when_ready():
    print('server starting...')
    #  通过监听端口的方式来验证服务已启动成功
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    if result == 0:
        # 已启动
        print('server started !')
        address = f'http://{get_ip()}: {port}'
        print(f'注册地址:{address}')
        registry(address=address)
    else:
        time.sleep(2)
        when_ready()


# 监测flask启动
threading.Thread(target=when_ready).start()


def registry(address):
    """注册当前执行器

    Args:
        address (_type_): 当前执行器地址 ip:port
    """
    registry_data = {'registryGroup': 'EXECUTOR',
                     'registryKey': app_name,
                     'registryValue': address
                     }
    print(job_admin_uri)
    res = requests.post(f'{job_admin_uri}/api/registry',
                        headers=req_headers, data=json.dumps(registry_data))
    # resp = json.loads(res.content)
    print('注册结果: '+str(res.content))
    start_timer(address=address)


def start_timer(address):
    """开启一个定时器
    """
    timer = Timer(15.0, registry, args=[address])
    timer.start()


def get_ip():
    """获取机器ip地址
    """
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('8.8.8.8', 80))
        ip = st.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        st.close()
    return ip


def unregister():
    """Called just before exiting Gunicorn.
   退出前执行调度中心摘除 TODO
   Args:
       server (_type_): 服务实例
   """
    if timer != None:
        timer.cancel()
        registry_data = {'registryGroup': 'EXECUTOR',
                         'registryKey': app_name,
                         'registryValue': address
                         }
        res = requests.post(f'{job_admin_uri}/api/registryRemove',
                            headers=req_headers, data=json.dumps(registry_data))
        print('摘除结果: ' + str(res.content))
# endregion -------------------------------------


if __name__ == '__main__':
    # 仅测试使用，正常会使用waitress来启动
    app.run(debug=True, host='0.0.0.0', port=9002)
