from forex_python.converter import CurrencyRates
from sqlalchemy.sql import True_
import ccxt

def getPrice(crypto, symbol, ticker, fp1, fp2):
    if crypto:
        exchange = ccxt.binance()
        t = exchange.fetch_ticker(symbol)
        return t[ticker]
    else:
        c = CurrencyRates();
        return (c.get_rate(fp1, fp2))
