from . import web

__author__ = '七月'


# def __current_user_status_change():
#     r = request


@web.route('/')
def index():
    return 'hello'


@web.route('/personal')
def personal_center():
    pass
