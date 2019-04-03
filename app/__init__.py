"""
完成应用级别的初始化操作，包括创建app，注册蓝图
"""
from flask import Flask
from app.models.base import db
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)  # 实例化Flask
    # config本身就是dict的子类
    app.config.from_object('app.secure')  # 接受模块路径，载入配置文件
    app.config.from_object('app.setting')  # 接受模块路径，载入配置文件
    register_blueprint(app)  # 给app注册蓝图
    db.init_app(app)  # 关联app
    login_manager.init_app(app)  # login_manager初始化
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    db.create_all(app=app)  # 让sqlAlchemy把所有的数据模型映射到数据库里，如果不调用不会生成数据表
    return app


def register_blueprint(app):
    # 用于注册蓝图
    from app.web import web
    app.register_blueprint(web)
