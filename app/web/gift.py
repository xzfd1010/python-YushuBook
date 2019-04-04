from flask import current_app, flash, redirect, url_for

from app.models.base import db
from app.models.gift import Gift
from . import web
from flask_login import login_required, current_user

__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    return 'My Gifts'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # isbn需要验证，验证函数写在user的方法中，将它视为用户的行为，好处：复用性更强；放到form校验中不好复用
    if current_user.can_save_to_list(isbn):
        # 事务
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id  # current_user是一个实例化后的User模型，flask_login通过get_user获取到current_user
            ###########
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
