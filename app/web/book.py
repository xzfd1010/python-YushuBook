from flask import jsonify, request

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YushuBook
from . import web
from app.forms.book import SearchForm


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
    if form.validate():  # 执行校验
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        # 不可变转可变 test3.py = request.args.to_dict()  args是一个immutable dict
        if isbn_or_key == 'isbn':
            result = YushuBook.search_by_isbn(q)
        else:
            result = YushuBook.search_by_keyword(q, page)
        return jsonify(result)
    else:
        return jsonify(form.errors)
        # return json.dumps(result), 200, {'content-type': 'application/json'}

# app.add_url_rule('/hello/', view_func=hello)  # 视图函数
