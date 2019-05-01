from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, ChangePasswordForm
from app.models.base import db
from app.models.user import User
from . import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

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
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            from app.libs.email import send_mail
            send_mail(form.email.data, '重置你的密码', 'email/reset_password.html', user=user, token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_email + '，请及时查收')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    print('data', form.data)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('修改密码成功')
            return redirect(url_for('web.login'))
        else:
            flash('修改密码失败')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user.password = form.new_password1.data
        db.session.commit()
        flash('密码已更新成功')
        return redirect(url_for('web.personal_center'))
    return render_template('auth/change_password.html', form=form)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))


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
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        form = RegisterForm()
        form.validate()
        user = User(form.nickname.data,form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'email/confirm', user=user, token=token)
        login_user(user, False)
        g.status = True
        flash('一封激活邮件已发送至您的邮箱，请快完成验证', 'confirm')
        # 由于发送的是ajax请求，所以redirect是无效的
        return 'go to index'
