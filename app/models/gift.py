from collections import namedtuple

from flask import current_app
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func

from app.spider.yushu_book import YushuBook

EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])


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

    def is_yourself_gift(self, uid):
        return self.uid == uid

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn，到Wish表中计算出某个礼物的Wish心愿数
        # 需要拿到一组数量，所以拿到总数量之后，需要分组求数量，group_by，
        # 不是查询模型，而是数量
        # 保存用到了db.session，也可以用于查询
        # filter的查询，是根据条件查询，传入条件表达式
        # func.count + group_by = 分组统计
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        # 返回对象
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

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

    def delete(self):
        self.status = 0
