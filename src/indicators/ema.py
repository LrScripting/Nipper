def getEMA(data, window):
    ema = []
    sma = sum(data[:window]) / window
    ema.append(sma)
    for i in range(window, len(data)):
        ema.append((data[i] * (2 / (window + 1))) + (ema[-1] * (1 - (2 / (window + 1)))))
    return ema[-1]
