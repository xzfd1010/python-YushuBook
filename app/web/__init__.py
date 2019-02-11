"""
完成蓝图级别的初始化操作
"""
from flask import Blueprint

web = Blueprint('web', __name__)
print(__name__)

# 引入模块，执行，注册视图函数
from . import book
