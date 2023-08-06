#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
执行器实现
@author: alex
@date:   2022/05/21 
"""

import threading
import logging
import queue
import requests
import json
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from helper import SUCCESS_RESP, TriggerParam, response_err, create_logger, clear_logger
from helper import job_admin_uri, job_admin_access_token
from ast import literal_eval
logger = logging.getLogger('main.Executor')

# key: job_id value: JobThread
job_threads = dict()

"""
job执行线程类
"""


class JobThread(threading.Thread):

    '''
    执行的队列 对于相同任务的多次触发 会先进入该队列 串行执行
    '''
    __q: queue.Queue

    '''
    队列长度
    '''
    __q_max_size: int = 1024

    '''
    线程终止信号 默认false
    '''
    __stop_signal: bool = False

    '''
    线程终止原因 为空则表示正常退出
    '''
    __stop_reason: str = ''

    '''
    是否正在执行任务
    '''
    __running: bool = False

    '''
    日志id集合 避免重复执行同一个参数
    '''
    __log_id_set: set = set()

    '''
    线程池
    '''
    __pool: ThreadPoolExecutor = None

    def __init__(self, job_id, daemon: bool = True):
        """构造一个job 线程

        Args:
            job_id (_type_): 任务执行id
            daemon (bool, optional): 是否是 daemon. Defaults to True.
       """
        threading.Thread.__init__(self)
        core_num = multiprocessing.cpu_count()
        logger.info(f'单个任务并发数(cpu): {core_num}')
        # super().__init__(self)
        self.daemon = daemon
        self.name = f'job-thread-{job_id}'
        self.__q = queue.Queue(maxsize=self.__q_max_size)
        self.__pool = ThreadPoolExecutor(
            max_workers=core_num, thread_name_prefix=self.name+'-executor')

    def run(self):
        logger.info("开始线程：" + self.name)
        while not self.__stop_signal:
            self.__running = False
            try:
                trigger_param = self.__q.get(block=False)
            except:
                continue
            handler = str(trigger_param.executor_handler)
            # 创建本次任务执行日志
            job_logger = create_logger(
                job_handler_name=handler, job_log_id=trigger_param.log_id)
            job_logger.info(f'{trigger_param}')
            try:
                self.__log_id_set.discard(trigger_param.log_id)
                self.__running = True
                dot_last_idx = handler.rindex('.')
                class_name = handler[:dot_last_idx] if dot_last_idx > 0 else handler
                method_name = handler[dot_last_idx +
                                      1:] if dot_last_idx > 0 else 'run'
                print(f'class: {class_name}, method: {method_name}')
                # 动态获取job目录
                module = __import__(
                    'executor.job.{}'.format(class_name), fromlist=True)
                params = str(trigger_param.executor_params).lstrip().rstrip()
                job_logger.info('开始执行模块 {}, 方法 {}, 参数: {}'.format(
                    module, method_name, params))
                future = None
                result = None
                if hasattr(module, method_name):
                    func = getattr(module, method_name)
                    if params.startswith('{'):
                        future = self.__pool.submit(
                            func, **literal_eval(params))
                    elif params.find('=') > 0:
                        future = self.__pool.submit(func, **dict(e.lstrip().split('=')
                                                                 for e in params.split(',')))
                    else:
                        future = self.__pool.submit(func, params)
                #  默认执行超时 1小时
                timeout_secs = 3600
                if trigger_param.executor_timeout is not None and trigger_param.executor_timeout > 0:
                    timeout_secs = int(trigger_param.executor_timeout)
                try:
                    result = future.result(timeout=timeout_secs)
                except Exception as ex_info:
                    job_logger.info(
                        f'<br>-----------job execute error {ex_info}')
                    future.cancel()
                    callback(trigger_param.log_id, False, '执行异常终止')
               # quit()

            except RuntimeError as err_info:
                # 记录错误
                job_logger.error(f'execute error: {err_info}')
                callback(trigger_param.log_id, False, f'{err_info}')
                # raise Exception(err)
            size = self.__q.qsize()
            logger.info(f'本次处理完成, 待处理队列长度: {size}')
            callback(trigger_param.log_id, True, '执行成功', result)
            clear_logger(handler)
            
            # size =0 则stop该线程
            if size == 0:
                del job_threads[trigger_param.job_id]
                self.stop(f'{self.name} 执行完成')

        # TODO: callback fail
        logger.info(
            f'退出线程: {self.name} 原因: {self.__stop_reason}, 运行线程数: {threading.activeCount()}')

    def stop(self, reason=None):
        """从外部停止线程
        Args:
            reason (_type_, optional): 停止原因. Defaults to None.
        """
        if self.isAlive():
            print('stopping...')
            self.__stop_signal = True
            self.__stop_reason = reason
        else:
            logger.info(f'{self.name} 已停止')

    def push(self, param: TriggerParam):
        """放入执行队列 等待执行

        Args:
            param (TriggerParam): 执行参数

        Raises:
            Exception: 当队列已满时 抛出异常
        """
        if self.__q.qsize() >= self.__q_max_size:
            raise Exception(f'{self.name} 队列已满')

        self.__log_id_set.add(param.log_id)
        self.__q.put(param)
        return self.__q.qsize()

    def isRunningOrHasQueue(self):
        return self.__q.qsize() > 0 or self.__running

    def isReady(self, logId):
        """当前参数正在队列中 此时不应该再push

        Args:
            logId (_type_): 参数中的日志id
        """
        return logId in self.__log_id_set


def run(param: TriggerParam):
    """执行对应的job 

    Args:
        param (TriggerParam): 本次执行参数
    """
    job_id = param.job_id
    if job_id is None:
        return response_err('jobId 不能为空')

    my_thread: JobThread = job_threads.get(job_id)
    count = threading.activeCount()
    logger.info(
        f'正在运行的线程数: {count}, 执行任务id: {job_id}, job_threads size: {len(job_threads)}')
    if my_thread is None:  # or not my_thread.isAlive()
        # logger.info(f'thread is alive: {my_thread.isAlive()}')
        my_thread = JobThread(job_id=job_id)
        # 判断是否重复执行同一参数
        if my_thread.isReady(param.log_id):
            return response_err(f'重复的执行参数,log id: {param.log_id}')
        my_thread.push(param=param)
        job_threads[job_id] = my_thread
        my_thread.start()
    else:
        # 判断block策略 丢弃当前
        if 'DISCARD_LATER' == param.block_strategy and my_thread.isRunningOrHasQueue():
            return response_err('前一任务正在执行，根据设置的策略，本次任务被丢弃')
        else:
            # 判断是否重复执行同一参数
            if my_thread.isReady(param.log_id):
                return response_err(f'重复的执行参数,log id: {param.log_id}')
            my_thread.push(param=param)
    return SUCCESS_RESP


def idle_beat(jobId):
    logger.info(f'空闲检测jobId: {jobId}')
    my_thread: JobThread = job_threads.get(jobId)
    if my_thread is not None and my_thread.isAlive() and my_thread.isRunningOrHasQueue():
        return response_err('job thread is running or has trigger queue.')
    return SUCCESS_RESP


def kill(jobId: int):
    """终止对应的线程

    Args:
        jobId (int): 任务id
    """
    logger.info(f'终止任务jobId: {jobId}')
    my_thread: JobThread = job_threads.get(jobId)
    if my_thread is not None and my_thread.isAlive():
        my_thread.stop(reason='Stopped by xxl-job-admin')
        if my_thread.isRunningOrHasQueue() == False:
            del job_threads[jobId]
    pass


def callback(log_id: int, success: bool, msg: str, result: any = None):
    """结果回调 TODO
    """
    req_headers = {}
    if job_admin_access_token is not None:
        req_headers = {'XXL-JOB-ACCESS-TOKEN': job_admin_access_token}
    res = requests.post(f'{job_admin_uri}/api/callback',
                        headers=req_headers, data=json.dumps([{
                            'logId': log_id,
                            'handleCode': 200 if success == True else 500,
                            'handleMsg': msg,
                            'handleResult': result
                        }]))
    print(str(res.content))
