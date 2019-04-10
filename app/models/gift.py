from flask import current_app
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc

from app.spider.yushu_book import YushuBook


class Gift(Base):
    # 连接user和book
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))  # 小写是因为代表user.id, ForeignKey 代表外键
    # book = relationship('Book')
    # bid = Column(Integer,ForeignKey('book.id'))  # 数据库没有存放书籍数据
    # 用isbn编号将book和user关联
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)  # 代表礼物是否赠送成功

    @classmethod
    def recent(cls):
        # 换行在括号处换行, 不会出现反斜杠
        # limit 控制数量,
        # order_by 排序, 排序在限制个数之前
        # distinct 去重, 需要先分组  group_by(Gift.isbn)
        # 链式调用
        recent_gift = Gift.query.filter_by(
            launched=False).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()  # 选取未被赠送的书籍
        return recent_gift

    # 根据isbn取book
    @property
    def book(self):
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
