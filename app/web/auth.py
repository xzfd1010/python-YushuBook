from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User
from . import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            # 不一个一个赋值，如何简化？ 利用python动态语言的特性
            user.set_attrs(form.data)
            # 将模型存入到数据库中，session是什么
            db.session.add(user)
            # 错误在form的error下

            # 跳转到其他视图函数，这是一次重定向
            return redirect(url_for('web.login'))

    # 如果想要提交后保存用户的提交信息，要把form重新传进去
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        user = User.query.filter_by(email=form.email.data).first()
        # 校验用户是否存在，密码是否相同
        if user or user.check_password(form.password.data):
            # 登陆成功颁发票据，并写入cookie，使用flask的插件 flask-login
            login_user(user, remember=True)
            next_url = request.args.get('next')
            if not next_url or next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass


@web.route('/register/confirm/<token>')
def confirm(token):
    pass
    # if current_user.confirmed:
    #     return redirect(url_for('main.index'))
    # if current_user.confirm(token):
    #     db.session.commit()
    #     flash('You have confirmed your account. Thanks!')
    # else:
    #     flash('The confirmation link is invalid or has expired.')
    # return redirect(url_for('main.index'))


@web.route('/register/ajax', methods=['GET', 'POST'])
def register_ajax():
    pass
