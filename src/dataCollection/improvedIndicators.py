import pandas as pd
import warnings 
import ta

class Indicators:
    def __init__(self, currPair, timeframes):
            self.pricesArr = []
            # make function which grabs dependant on time frame and currency pair
            self.prices = pd.DataFrame(pd.read_csv("./EURUSD1.csv", delimiter="\t", names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume']))
            self.prices = self.prices.drop(columns='Date')
            self.finalArr = []
            self.batchSizes = 100
            self.dataLength = 1000
            self.lastArr = []
            self.prices['EMA'] = None
            

    def genData(self, length, batchSize):
        
        for i in range(0, length, batchSize):
            data = pd.DataFrame(self.prices.iloc[i:i+batchSize])
            data = data.astype({"Open": float, "High": float, "Low": float, "Close": float, "Volume": float})

            self.pricesArr.append(data)
    
    def predictionBatch(self, data, short_period=12, long_period=26, signal_period=9):
        data['EMA'] = ta.trend.ema_indicator(data['Close'])
        data["bbHigh"] = ta.volatility.bollinger_hband_indicator(data['Close'])
        data['bbLow'] = ta.volatility.bollinger_lband_indicator(data['Close'])
        data['ADX'] = ta.trend.adx(data['High'], data['Low'], data['Close'])
        data['RSI'] = ta.momentum.rsi(data['Close'])
        
        macd_line, signal_line, macd_hist = ta.trend.macd(data['Close'], n_fast=short_period, n_slow=long_period, fillna=False)
        data['MACD'] = macd_hist
        return data
 
    def generateSupportResistance(self, vol_period=10, ema_period=20, buffer_percent=0.01):
        for i in range(len(self.pricesArr)):
            batch = self.getBatch(i, ema_period + vol_period - 1)
            
            # Calculate recent volatility (high - low) as a proxy for price swings
            batch['Volatility'] = batch['High'].rolling(window=vol_period).max() - batch['Low'].rolling(window=vol_period).min()
            
            # Use volatility to determine dynamic window size, default to vol_period if volatility is zero
            batch['Window'] = (batch['Volatility'] / batch['Volatility'].mean()).apply(lambda x: max(int(x), vol_period))
            
            # Calculate exponential moving average of highs and lows as potential support and resistance
            batch['Resistance'] = batch['High'].ewm(span=ema_period).mean()
            batch['Support'] = batch['Low'].ewm(span=ema_period).mean()

            # Add a buffer to create a "zone" instead of a single price level
            batch['Resistance'] = batch['Resistance'] * (1 + buffer_percent)
            batch['Support'] = batch['Support'] * (1 - buffer_percent)

            start_idx = ema_period if i != 0 else 0
            self.pricesArr[i].loc[batch.index[start_idx:], ['Resistance', 'Support']] = batch[['Resistance', 'Support']][start_idx:]

    def bgenerateSupportResistance(self):
        for i in range(len(self.pricesArr)):
            batch = self.getBatch(i, 24) # assuming 24 data points in a day for 1m bars
            batch['Resistance'] = batch['High'].rolling(window=24).max()
            batch['Support'] = batch['Low'].rolling(window=24).min()
            start_idx = 24 if i != 0 else 0
            self.pricesArr[i].loc[batch.index[start_idx:], ['bResistance', 'bSupport']] = batch[['bResistance', 'bSupport']][start_idx:]

    def getBatch(self, i, periods):
        if i == 0:
            batch = self.pricesArr[i].copy()
        else:
            batch = pd.concat([self.pricesArr[i-1].iloc[-periods:],self.pricesArr[i]]).copy()
        return batch

    def generateEMA(self, periods=20):
        
        for i in range(len(self.pricesArr)):  # using self.finalArr to loop over batches
                # Check if it's the first batch
            batch = self.getBatch(i, periods) 
            # calculate EMA on the batch
            batch['EMA'] = ta.trend.ema_indicator(batch['Close'], window=periods)

            # Update the original DataFrame with the calculated EMA, skip the first 'periods' rows if it's not the first batch
            start_idx = periods if i != 0 else 0
            self.pricesArr[i].loc[batch.index[start_idx:], 'EMA'] = batch['EMA'][start_idx:]

    def genBollingerBands(self, periods=20, windowDev=2):

        for i in range(len(self.pricesArr)):
            batch = self.getBatch(i, periods)            
            batch["bbHigh"] = ta.volatility.bollinger_hband_indicator(batch['Close'], window=periods, window_dev=windowDev)
            batch['bbLow'] = ta.volatility.bollinger_lband_indicator(batch['Close'], window=periods, window_dev=windowDev)
            start_idx = periods if i != 0 else 0
            self.pricesArr[i].loc[batch.index[start_idx:], ['bbHigh', 'bbLow']] = batch[['bbHigh', 'bbLow']][start_idx:]



    def generateADX(self, periods=14):

        warnings.filterwarnings("ignore", category=RuntimeWarning)
        for i in range(len(self.pricesArr)):
            # Check if it's the first batch
            batch = self.getBatch(i, periods)            
            # calculate ADX on the batch
            batch['ADX'] = ta.trend.adx(batch['High'], batch['Low'], batch['Close'], window=periods)

            # Update the original DataFrame with the calculated ADX, skip the first 'periods' rows if it's not the first batch
            start_idx = periods if i != 0 else 0
            self.pricesArr[i].loc[batch.index[start_idx:], 'ADX'] = batch['ADX'][start_idx:]
    
    def generateRSI(self, periods=14):
        for i in range(len(self.pricesArr)):
            # Check if it's the first batch
            batch = self.getBatch(i, periods)            
            # Calculate RSI on the batch
            batch['RSI'] = ta.momentum.rsi(batch['Close'], window=periods)

            # Update the original DataFrame with the calculated RSI, skip the first 'periods' rows if it's not the first batch
            start_idx = periods if i != 0 else 0
            self.pricesArr[i].loc[batch.index[start_idx:], 'RSI'] = batch['RSI'][start_idx:]


    def generateMACD(self, short_period=12, long_period=26, signal_period=9):
        for i in range(len(self.pricesArr)):
            # Check if it's the first batch
            batch = self.getBatch(i, short_period + long_period - 1)
            # Calculate MACD on the batch
            macd_line, signal_line, macd_hist = ta.trend.macd(batch['Close'], n_fast=short_period, n_slow=long_period, fillna=False)

            # Update the original DataFrame with the calculated MACD, skip the first 'long_period' rows if it's not the first batch
            start_idx = long_period if i != 0 else 0
            self.pricesArr[i].loc[batch.index[start_idx:], 'MACD'] = macd_hist[start_idx:]

    def updateBatch(self, newBatch):
        self.pricesArr.pop(0)
        self.pricesArr.append(newBatch)
    
    def saveBatches(self, fileName):
        allData = pd.concat(self.pricesArr, ignore_index=True)
        allData.to_csv(fileName, sep='\t', index=False)






        

ind = Indicators("USD", "LOL")
ind.genData(1000, 100)
ind.generateEMA()
ind.generateRSI()
ind.generateMACD()
ind.generateADX()
ind.genBollingerBands()
print(ind.pricesArr)
