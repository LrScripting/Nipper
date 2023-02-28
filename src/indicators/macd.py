def calculateMACD(arr, slow_period=26, fast_period, signal_period):
    ema_slow = calculateEMA(arr, slow_period)
    ema_fast = calculateEMA(arr, fast_period)
    macd = ema_fast - ema_slow
    signal_line = calculateEMA(macd, signal_period)
    histogram = macd - signal_line
    return (macd, signal_line, histogram)
