# sqlalchemy 生成sql语句的包，非python独有
# Flask_SQLAlchemy flask封装的，API更人性化
# WTForms
# Flask_WTFORMS

# Flask
# werkzeug

from sqlalchemy import Column, Integer, String  # 基本类型从sqlalchemy导入
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键、自增
    title = Column(String(50), nullable=False)  # 长度50，不为空
    author = Column(String(30), default='佚名')
    binding = Column(String(20))  # 装帧
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)  # unique_key 唯一键
    summary = Column(String(1000))
    image = Column(String(50))

    def sample(self):
        pass
