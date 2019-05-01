from flask import current_app, flash, redirect, url_for, render_template

from app.libs.enum import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from app.view_models.trade import MyTrades
from . import web
from flask_login import login_required, current_user

__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)  # 用户的礼物清单
    # 需要查询想要书籍的人数
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


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
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid,launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid,pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))


