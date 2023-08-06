'''
Author: Alex
LastEditors: Alex yxfacw@163.com
Date: 2023-07-19 10:05:05
Description:  仅测试用 pip 包的方式会在应用的py中调用 
'''

from waitress import serve
from flask import Flask
from main import app
from helper import port

serve(app, host='0.0.0.0', port=9002)