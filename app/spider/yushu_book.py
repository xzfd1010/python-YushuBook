"""
处理当前程序的所有请求
"""
from app.libs.my_http import HTTP
from flask import current_app  # 当前的app核心对象


class YushuBook:
    '''
    完成所有的请求
    类有职责自身完成请求，所以url应该定义为类变量
    '''
    # {} 代表动态参数
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    # 传入各自需要的参数
    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)  # self.isbn_url也可以找到，链式查找
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        url = cls.keyword_url.format(keyword, current_app.config['PER_PAGE'], cls.calculate_start(page))
        result = HTTP.get(url)
        return result

    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config['PER_PAGE']
