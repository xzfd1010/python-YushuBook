"""
解决的问题：
    统一search视图函数的数据结构
    补全关键字信息
"""


class BookViewModel:
    def __init__(self, book):
        # 先处理单本数据，再处理集合数据
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''  # None转为空字符串
        self.author = '、'.join(book['author'])  # 单页面应用建议用js操作；如果是网站，建议在viewModel中处理
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.image = book['images']
        self.isbn = book['isbn']

    @property  # 用属性访问的方式访问函数
    def intro(self):
        # 过滤规则由lambda表达式决定，返回True，就会进入intros，返回False，就会过滤掉
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


# 不好的写法，废弃
class _BookViewModel:
    # 这个class没有必要存在（伪面向对象）如果有大量的可以被标注为classmethod、staticmethod的方法，就并没有真正的面向对象
    # 面向对象应该描述特征（类标量、实例变量）
    # 描述行为（方法）
    # 理解不到位，很容易写出只有方法、没有变量的类
    # 只有方法的类，实际上是面向过程

    @classmethod
    def package_single(cls, data, keyword):  # data原始数据，keyword 关键字
        # 返回单本书

        # 统一的数据结构
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = cls.__cut_book_data(data)
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        # 返回多本书

        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]  # 复用单个书籍的处理方法，是一种经典方法
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        # 裁剪原始数据
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',  # None转为空字符串
            'author': '、'.join(data['author']),  # 单页面应用建议用js操作；如果是网站，建议在viewModel中处理
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['images']
        }
        return book
