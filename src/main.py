import ccxt
from collections import deque
import time
import numpy as np
import pandas as pd
from requests import get
import ta
from settingsClass import Settings
from getPrice import getPrice
from Account import Account
from pastPriceFX import passedPriceFX
from shorttermIndicators.ema import Ema
from shorttermIndicators.macd import Macd
from shorttermIndicators.sma import Sma
from shorttermIndicators.stoch import Stoch
from shorttermIndicators.dx import Der 




exchange = ccxt.binance()
userSettings = Settings()
userAcc = Account(userSettings.tradeSettings['sBalance'], userSettings.tradeSettings['buyAmount'])
startBalance = userSettings.tradeSettings['sBalance']


#initialize passed data



# Create the deques to store the most recent price data for analysis
# initialized and fill default deque
priceData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))))
for i in range(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))):
    priceData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][0], userSettings.market['forexPair1'], userSettings.market['forexPair2']))

#initialize optional deques if chosen
if userSettings.dataSettings['dataColl'][0]['high']: 
    highData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))))
    for i in range(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))):
        highData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][1], userSettings.market['forexPair1'], userSettings.market['forexPair2']))
if userSettings.dataSettings['dataColl'][2]['low']: 
    lowData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))))
    for i in range(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))):
        lowData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][2], userSettings.market['forexPair1'], userSettings.market['forexPair2']))
if userSettings.dataSettings['dataColl'][3]['closed']: 
    closedData = deque(maxlen=(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))))
    for i in range(int(str(userSettings.dataSettings['timeframes'][0]["5Min"]))):
        closedData.append(getPrice(userSettings.market['crypto'], userSettings.market['symbol'], userSettings.market['tickers'][3], userSettings.market['forexPair1'], userSettings.market['forexPair2']))

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
        if ema(data, settings) > sma(data, settings) and der(data) > threshhold:

            tradePrice = price
            userAcc.balance -= userSettings.tradeSettings['buyAmount']
            userAcc.balance -= userSettings.tradeSettings['fee']
            userAcc.inTrade = True
            userAcc.tradeNumber +=1
                       
    time.sleep(1)
