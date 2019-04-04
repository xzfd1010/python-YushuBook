from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String


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
