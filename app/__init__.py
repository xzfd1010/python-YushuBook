"""
完成应用级别的初始化操作，包括创建app，注册蓝图
"""
from flask import Flask


def create_app():
    app = Flask(__name__)  # 实例化Flask
    # config本身就是dict的子类
    app.config.from_object('app.secure')  # 接受模块路径，载入配置文件
    app.config.from_object('app.setting')  # 接受模块路径，载入配置文件
    register_blueprint(app) # 给app注册蓝图
    return app


def register_blueprint(app):
    # 用于注册蓝图
    from app.web import web
    app.register_blueprint(web)
