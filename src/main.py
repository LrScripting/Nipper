import ccxt
from collections import deque
import time
from ccxt.base.decimal_to_precision import decimal
#import numpy as np
#import pandas as pd
from requests import get
#import ta
from config.SettingsClass import Settings
from dataCollection.getPrice import getPrice
from config.AccountClass import Account
from dataCollection.pastPriceFX import passedPriceFX
from dataCollection.pastPriceCrypto import passedPriceCrypto
#from shorttermIndicators.ema import Ema
#from shorttermIndicators.macd import Macd
#from shorttermIndicators.sma import Sma
#from shorttermIndicators.stoch import Stoch
#from shorttermIndicators.dx import Der
from decimal import Decimal
from indicators.der import maDX  
from indicators.ema import getEMA
from indicators.sma import getSMA

#Into

print("""Starting Nipper...""")

time.sleep(1)
exchange = ccxt.binance()
userSettings = Settings()
userAcc = Account(userSettings.tradeSettings['sBalance'], userSettings.tradeSettings['buyAmount'])
startBalance = userSettings.tradeSettings['sBalance']


print("""Loading Past Data...""")
#initialize indicator data

if userSettings.market['crypto']:
#last 100 price points
    oldpriceArr = passedPriceCrypto(exchange, userSettings.market['symbol'], 100)
else:
    oldpriceArr = passedPriceFX('GBP', 'USD', 100)

ema = getEMA(oldpriceArr, 20)
smaLong = getSMA(oldpriceArr, 50)

print("""Loading Live Market Data....""")
# Create the deques to store the most recent price data for analysis
# initialized and fill default deque
priceData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))))
for i in range(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))):
    priceData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][0], userSettings.market['forexPair1'], userSettings.market['forexPair2']))

#initialize optional deques if chosen
if userSettings.dataSettings['dataColl'][0]['high']:
    highData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))))
    for i in range(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))):
        highData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][1], userSettings.market['forexPair1'], userSettings.market['forexPair2']))
if userSettings.dataSettings['dataColl'][2]['low']:
    lowData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))))
    for i in range(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))):
        lowData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][2], userSettings.market['forexPair1'], userSettings.market['forexPair2']))
if userSettings.dataSettings['dataColl'][3]['closed']:
    closedData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))))
    for i in range(int(str(userSettings.dataSettings['timeframes'][1]["5Min"]))):
        closedData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][3], userSettings.market['forexPair1'], userSettings.market['forexPair2']))


print(f"""
    --BOT ONLINE-- 
    Start Balance: {userAcc.balance}
    Bot Mode {userSettings.market['crypto']}
    Good Luck!""")
time.sleep(2)



#initialize tradePrice
tradePrice = 0

while True:
   
    #Reset Count at start of each iteration
    counter = 0
   

    #get Price
    price = getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][0], userSettings.market['forexPair1'], userSettings.market['forexPair2'])
   
    # Make Data suitable for the indicator functions
    priceData.append(price)    
   

    if userAcc.inTrade:

        print(f"""In Trade! Buy in Price: {tradePrice},
    current profit {int(tradePrice) - price}, overall profit {userAcc.balance - startBalance}
          Balance: {userAcc.balance}""")
        if price >= tradePrice * userSettings.tradeSettings['buyoutRatio']:
            userAcc.balance = userAcc.balance * userSettings.tradeSettings['buyoutRatio']
            userAcc.balance += userSettings.tradeSettings['buyAmount']
            userAcc.inTrade = False
        if  price <= tradePrice * userSettings.tradeSettings['buyoutRatio']:
            userAcc.balance = userAcc.balance * userSettings.tradeSettings['sellRatio']

    else:
        print(f"""Not in Trade. Balance: {userAcc.balance}, session Profit {userAcc.balance - startBalance}""")
        #if userSettings.indicators['ema']: counter += Ema()
        #if userSettings.indicators['sma']: counter+=Ema()
        #if userSettings.indicators['der']: counter +=Der()
        ##if counter >= userSettings.tradeSettings['buyThreshold']:
        liveEMA = ((Decimal(price) * Decimal((2 / (14 + 1)))) + Decimal(ema * (1 - (2 / (14 + 1)))))
        if liveEMA > smaLong and maDX(priceData, userSettings.indicatorSettings['der'][0]['window'] ) > userSettings.indicatorSettings['der'][1]['threshold']:


            tradePrice = price
            userAcc.balance -= userSettings.tradeSettings['buyAmount']
            userAcc.balance -= userSettings.tradeSettings['fee']
            userAcc.inTrade = True
            userAcc.tradeNumber +=1
                       
    time.sleep(1)
