from sqlalchemy.orm import relationship
from app.models.base import Base, db
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func

from app.spider.yushu_book import YushuBook


class Wish(Base):
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
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        # 返回对象
        count_list = [{'count': g[0], 'isbn': g[1]} for g in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    def delete(self):
        self.status = 0
