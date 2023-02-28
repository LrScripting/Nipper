class Account:
    def __init__(self, balance, buyParam):
        self.balance = balance
        self.tradeNumber = 0
        self.inTrade = False
        self.buyParam = buyParam
    
