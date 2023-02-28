def getSMA(data, window):
    return(sum(data[-window:]) / window)
