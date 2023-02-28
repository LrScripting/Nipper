
class Settings:
    def __init__(self):

        self.market = {
                "crypto": False,       
                "symbol": "BTC/USD",
                "tickers": ["last", 'high', 'low', 'close'],
                "forexPair1": "USD",
                "forexPair2": "GBP"
        }
        self.dataSettings =  {"timeframes": [ {"3Min": 180}, {"5Min": 300}, {"10Min": 600}, {"15Min": 900}],
                              "dataColl": [{"high": False}, {"price": True}, {'low': False}, {"closed": False}]}
        self.indicators = {
                "sma": True,
                "ema": True,
                "rsi": False,
                "tsi": False,
                "Macd": True,
                "stoch": True,
        }
        self.indicatorSettings = {
                "sma": [{"window": 50}],
                "ema": [{"window": 15}] ,
                "der": [{"window": 180}, {"threshold": 0.32}],
                "tsi": [{"s1": 1}, {"s2": 2}, {"s3": 3}],
                "macd": [{"s1": 1}, {"s2": 2}, {"s3": 3}],
                "stoch":[{"s1": 1}, {"s2": 2}, {"s3": 3}]
        }
        self.tradeSettings = {
        "sBalance": 2000,
        "buyAmount": 500,
        "fee": 1.001,
        "buyThreshold": 4,
        "buyoutRatio": 1.05,
        "sellRatio": 0.98
        }
