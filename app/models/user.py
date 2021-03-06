from math import floor

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.enum import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db

from sqlalchemy import Column, Integer, String, Boolean, Float

from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YushuBook

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, Base):
    # __tablename__ = 'user1'  # 指定表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=False)
    # 默认情况下，普通字段对应数据库字段，如果想改变数据库字段名称，比如_password对应password，可以用Column('name')指定
    _password = Column("password", String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)  # 鱼豆
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))  # 用于开发微信小程序
    wx_name = Column(String(32))

    @property  # 可以写入属 性，这是getter，如果想让某个属性是只读的，就让setter阻止写入
    def password(self):
        return self._password

    @password.setter  # 这是setter，raw代表原始密码
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 用于校验密码
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        # 判断是真实的isbn编号
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        # 判断数据库是否存在这本书
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不能同时成为赠送者和索要者

        # 既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        # 生成令牌
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    @property
    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_received_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_received_count / 2) <= floor(success_gifts_count) else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
