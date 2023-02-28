def calculateStochasticOscillator(high, low, close, period=14, smooth=3):
    highest_high = max(high[-period:])
    lowest_low = min(low[-period:])
    k = (close[-1] - lowest_low) / (highest_high - lowest_low) * 100
    d = calculateSMA(k, smooth)
    return (k, d)
