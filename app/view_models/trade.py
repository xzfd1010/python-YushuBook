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
