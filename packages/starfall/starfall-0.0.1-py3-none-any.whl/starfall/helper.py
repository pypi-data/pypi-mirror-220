#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具类
@author: alex
@date:   2022/05/25 
"""

import datetime
from logging import handlers
import os
import logging
import time
from werkzeug.datastructures import ImmutableDict
import configparser
import json
import logging.config

# region -----------------config----------------------

PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
print(f'root path: {PROJ_ROOT}')

# JOB_PATH = os.path.join(ROOT_PATH, 'job')
# print(f'job 目录： {JOB_PATH}')

# 从环境变量获取日志路径配置
RUNTIME_LOG_PATH = os.environ.get('LOG_PATH', os.path.join(PROJ_ROOT, 'log'))
# 自动创建日志目录
if os.path.exists(RUNTIME_LOG_PATH) == False:
    os.makedirs(RUNTIME_LOG_PATH)

# 解析日志配置
log_config = os.path.join(PROJ_ROOT, 'logging.json')
if os.path.exists(log_config):
    with open(log_config) as f:
        log_config_obj = json.load(f)
    logging.config.dictConfig(log_config_obj)

# 解析配置
parser = configparser.ConfigParser()
parser.read(os.path.join(PROJ_ROOT, 'conf.ini'))
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

# endregion -------------------------------------

# 无内容的成功响应
SUCCESS_RESP = ImmutableDict({
    "code": 200,
    "msg": None
})


job_loggers = dict()


def create_logger(job_handler_name, job_log_id):
    """创建一个 job logger

    Args:
        job_handler_name (_type_): handler 名称
        job_log_id (_type_): 日志 id
    """
    logger = JobLogger(jobHandler=job_handler_name + "-" +
                       str(job_log_id), logId=job_log_id).logger
    job_loggers[job_handler_name] = logger
    return logger


def get_logger(job_handler_name):
    return job_loggers.get(job_handler_name)


def clear_logger(job_handler_name):
    if job_handler_name in job_loggers:
        del job_loggers[job_handler_name]
    else:
        pass


def response_err(error):
    """失败响应

    Args:
        error (_type_): 异常或消息

    Returns:
        Dict: 响应结构体
    """
    return ImmutableDict({
        "code": 500,
        "msg": str(error)
    })


def response_ok(data):
    """成功响应

    Args:
        data (_type_): 返回的数据

    Returns:
        Dict: 响应结构体
    """
    return {
        'code': 200,
        'content': data
    }


def read_log_line(param):
    """读取日志行

    Args:
        param (_type_): @see LogParam

    Returns:
        _type_: 成功响应
    """
    log_id = param.log_id
    date_str = time.strftime("%Y%m%d", time.localtime(
        int(str(param.log_datetime)[0:-3])))
    log_file = os.path.join(
        log_root_path, 'jobhandler', date_str, f'{log_id}.log')
    print(log_file)
    log_list = ['']
    start_line = param.line_start_no
    if not os.path.exists(log_file):
        return response_ok({'logContent': 'readLog fail, logFile not exists', 'fromLineNum': start_line,
                          'toLineNum': 0, 'isEnd': True})
    line_no = 1
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
        line = file.readline()
        while line:
            if line_no >= start_line:
                log_list.append(line)
            line = file.readline()
            line_no += 1

    return response_ok({'fromLineNum': start_line, 'toLineNum': line_no, 'logContent': "\n".join(log_list), 'isEnd': False})


"""
任务日志类

"""


class JobLogger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, jobHandler, logId, level='info'):
        self.logger = logging.getLogger(jobHandler)
        format_str = logging.Formatter(
            '%(asctime)s.%(msecs)d %(levelname)s %(process)d --- [%(threadName)s] [%(name)s] %(filename)s:%(lineno)d %(message)s')  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        datestr = datetime.datetime.now().strftime('%Y%m%d')
        JOB_LOG_PATH = os.path.join(log_root_path, 'jobhandler', datestr)
        if os.path.exists(JOB_LOG_PATH) == False:
            os.makedirs(JOB_LOG_PATH)
        th = handlers.TimedRotatingFileHandler(
            filename=log_root_path + os.path.sep + "jobhandler" + os.path.sep +
            datetime.datetime.now().strftime('%Y%m%d') +
            os.path.sep + f'{logId}.log',
            when='D', backupCount=14, encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


"""任务调度参数类

"""


class TriggerParam:

    """
    任务 id
    """
    job_id = None

    """
    执行类型 
    """
    glue_type = ''

    """
    执行模块 `a.test` 表示执行 a.py 的 test 方法
    若是 `a` 则默认是 a.py 中的 run 方法
    """
    executor_handler: str

    """
    执行参数(文本)
    支持两种形式：
      假设, 对应函数参数 x、y:
    - json 形式 `{"x": 2, "y": 3}`
    - 参数指定形式 `x=2,y=3` 
    - 不是以上两种格式的参数 `2` 直接传入
    """
    executor_params = ''

    """
    执行超时时间 默认0 
    """
    executor_timeout: int = 0

    """
    阻塞策略
    """
    block_strategy = ''

    """
    log id
    """
    log_id = None

    data: dict = {}

    """
    私有属性
    """
    __p = 'private property'

    """
    构造函数
    """

    def __init__(self, jobId, glueType, executorHandler,
                 executorParams, executorBlockStrategy, executorTimeout,
                 logId, logDateTime, glueSource=None, glueUpdatetime=None, broadcastIndex=0, broadcastTotal=0):
        self.job_id = jobId
        self.glue_type = glueType
        self.executor_handler = executorHandler
        self.executor_params = executorParams
        self.executor_timeout = executorTimeout
        self.block_strategy = executorBlockStrategy
        self.log_id = logId

    def __str__(self):
        return f'''
    ==========执行参数================
    jobId: {self.job_id}, 
    type: {self.glue_type}, 
    handler: {self.executor_handler}, 
    params: {self.executor_params},
    block_strategy: {self.block_strategy}
    timeout: {self.executor_timeout}
    log_id: {self.log_id}
    =================================
    '''

    def p(self):
        return self.__p


"""
日志请求类
"""


class LogParam:
    """
    log id
    """
    log_id = None

    """
    日志时间
    """
    log_datetime = None

    """
    开始行数 默认 0
    """
    line_start_no: int = 0

    def __init__(self, logDateTim, logId, fromLineNum):
        self.log_id = logId
        self.log_datetime = logDateTim
        self.line_start_no = fromLineNum

    def __str__(self):
        return f'''
    ==========日志参数================
    datetime: {self.log_datetime}, 
    line_no: {self.line_start_no},
    log_id: {self.log_id}
    =================================
    '''
