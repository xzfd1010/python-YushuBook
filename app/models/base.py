# 完成初始化操作
from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Integer, Column, SmallInteger


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        # kwargs是一个字典
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # 调用原有的filter_by逻辑
        return super(Query, self).filter_by(**kwargs)  # **用来对args解包


# 可以传入自己定义的BaseQuery
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)  # 是否可以在这里设置datetime，不可以，在这里设置，时间就是类声明时的时间
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':  # 用于判断一个对象是否有某个属性
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
