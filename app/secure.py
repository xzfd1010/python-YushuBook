# 数据库、密码、app_key放到这里面
# 生产环境和开发环境的配置不同
# 此文件应该 gitignore

# SQLALCHEMY_BINDS用于配置多个数据库
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:zc000123@localhost:3306/fisher'  # 变量名不能修改，连接数据库
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'aaabbb'

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '417466521@qq.com'
MAIL_PASSWORD = 'haukhkvzahsdbidi'
