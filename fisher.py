"""
本文件作用，创建app示例，启动服务器
"""

from app import create_app

__author__ = "Nick"

app = create_app()

if __name__ == '__main__':  # 下面代码只在入口文件执行
    # 生产环境不会使用flask自带的服务器，生产环境使用nignx + uwsgi部署服务器，此时本文件只是一个模块，而非入口文件
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81)  # 小写也能读取。。如果都小写还会报错
