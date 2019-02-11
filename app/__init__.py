"""
完成应用级别的初始化操作
"""
from flask import Flask


def create_app():
    app = Flask(__name__)  # 实例化Flask
    # config本身就是dict的子类
    app.config.from_object('app.secure')  # 接受模块路径，载入配置文件
    app.config.from_object('app.setting')  # 接受模块路径，载入配置文件
    register_blueprint(app)
    return app


# 用于注册蓝图
def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
