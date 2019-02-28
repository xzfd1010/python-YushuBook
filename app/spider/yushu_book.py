"""
处理当前程序的所有请求
"""
from app.libs.my_http import HTTP
from flask import current_app  # 当前的app核心对象


class YushuBook:
    # 完成所有的请求
    # 类有职责自身完成请求，所以url应该定义为类变量
    # 落脚点在Book，而方法的返回值就是book，所以可以用book来描述这个类本身

    # 模型层 MVC M层

    # {} 代表动态参数
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    # 是否要存储查询参数？不要，YushuBook应该返回的是关于书籍的信息，让类的职责更明确

    def __init__(self):
        # 保存数据；把两种不同数据结构统一
        self.total = 0
        self.books = []

    # 传入各自需要的参数
    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)  # self.isbn_url也可以找到，链式查找；实例没有会查找类变量
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
        # 处理单本数据
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        # 处理集合数据
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']
