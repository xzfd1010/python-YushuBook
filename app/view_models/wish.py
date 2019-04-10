from .book import BookViewModel
from collections import namedtuple


# 这个viewModel的目的，将gift数据+想要人的数量 一同返回前端 将gift和count挂钩
# gifts_of_mine是用户的礼物清单，wish_count_list是(isbn,count)的对象列表

# 单个的MyGift的记录
# 标识id,书籍book,心愿数量wish_count
# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])  # 不方便序列化


class MyWishes:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []

        # 作为私有属性，使用方便
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()  # 不建议在方法中直接修改实例属性，在方法比较复杂时，不知道在哪一步造成了修改

    def __parse(self):
        # 将gifts_of_mine和wish_count_list解析，将gift和count连接
        temp_gifts = []

        # 简化多层嵌套的for...in循环，再定义一个函数
        # for gift in self.__gifts_of_mine:
        #     for wish_count in self.__wish_count_list:
        #         pass
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        my_gift = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return my_gift
