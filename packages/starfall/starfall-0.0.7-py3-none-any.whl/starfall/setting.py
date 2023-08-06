'''
Author: Alex
LastEditors: Alex yxfacw@163.com
Date: 2023-07-20 09:16:34
Description:  
'''

import os
import configparser
import logging.config
import json


port = 9002
app_name = 'starfall'
job_admin_uri = None
job_admin_access_token = None
runtime_log_path = None


def init(proj_path: str):
    # 初始化
    # 从环境变量获取日志路径配置
    global runtime_log_path, port, job_admin_uri, job_admin_access_token, app_name
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
------------------------------------------
    port: {port}
    name: {app_name}
    admin_uri: {job_admin_uri}
    access_token: {job_admin_access_token}
------------------------------------------
      ''')
