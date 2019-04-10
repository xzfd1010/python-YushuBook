from flask import render_template

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web

__author__ = '七月'


# def __current_user_status_change():
#     r = request


@web.route('/')
def index():
    recent_gifts = Gift.recent()  # 需要把礼物作为书籍显示出来
    # 模型只负责处理原始数据
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
