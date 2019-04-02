from flask import jsonify, request, render_template, flash

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YushuBook
from app.view_models.book import BookViewModel, BookCollection
from . import web  # 这里引入的web是在__init__文件中初始化的实例，如果有多个也可以继续引入
from app.forms.book import SearchForm
import json


# 将视图函数注册到蓝图上
@web.route('/book/search')  # router <q>动态参数
def search():  # controller 也叫视图函数，本质就是函数，用于控制mvc view视图
    """
        q :普通关键字/isbn查询 用代码区分
        page
        ?q=name&page=num
    """
    # 验证层
    form = SearchForm(request.args)
    books = BookCollection()  # 空数据

    if form.validate():  # 执行校验
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        # 不可变转可变 test3.py = request.args.to_dict()  args是一个immutable dict
        yushu_book = YushuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
    # 确保总能返回结果
    return render_template('search_result.html', books=books)


# 书籍详情页
@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu_book = YushuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    # wishes gifts
    return render_template('book_detail.html', book=book, wishes=[], gifts=[])


@web.route('/test1')
def test1():
    from flask import request
    from app.libs.none_local import n
    print(n.v)  # 原始值为1，修改之后应该变成2
    n.v = 2
    print(n.v)
    print('-------------')
    print(getattr(request, 'v', None))  # request中值不会变化
    setattr(request, 'v', 2)
    print(request.v)
    print('-------------')
    return ''


@web.route('/test')
def test():
    r = {
        'name': '',
        'age': 18
    }
    # 填充html，然后返回
    # 引入模板的概念，
    flash('hello,qiyue')
    return render_template('test.html', data=r)
