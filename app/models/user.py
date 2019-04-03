from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base

from sqlalchemy import Column, Integer, String, Boolean, Float


class User(UserMixin, Base):
    # __tablename__ = 'user1'  # 指定表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=False)
    # 默认情况下，普通字段对应数据库字段，如果想改变数据库字段名称，比如_password对应password，可以用Column('name')指定
    _password = Column("password", String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
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


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
