"""
完成蓝图级别的初始化操作
"""
from flask import Blueprint, render_template

web = Blueprint('web', __name__)  # 声明蓝图


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# 引入模块，执行，注册视图函数
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
