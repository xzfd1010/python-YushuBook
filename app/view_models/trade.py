from .book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    # 处理单个数据
    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')  # strftime格式化为年月日
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        # 作为私有属性，使用方便
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()  # 不建议在方法中直接修改实例属性，在方法比较复杂时，不知道在哪一步造成了修改

    def __parse(self):
        # 将trades_of_mine和trade_count_list解析，将trade和count连接
        temp_trades = []

        # 简化多层嵌套的for...in循环，再定义一个函数
        # for trade in self.__trades_of_mine:
        #     for trade_count in self.__trade_count_list:
        #         pass
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        # my_trade = MyGift(trade.id, BookViewModel(trade.book), count)
        my_trade = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return my_trade
