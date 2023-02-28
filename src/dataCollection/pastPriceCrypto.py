import ccxt
from datetime import datetime, timedelta
exchange = ccxt.binance()
def passedPriceCrypto(exchange, symbol, window):
    arr = []
    timeframe = '1d' # daily timeframe
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=window)

    # fetch OHLCV data for the given symbol and timeframe
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, int(start_time.timestamp() * 1000), int(end_time.timestamp() * 1000))

    # extract the closing prices from the OHLCV data
    for data in ohlcv:
        arr.append(data[4])

    return arr

