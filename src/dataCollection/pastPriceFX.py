import ccxt
from datetime import datetime
from forex_python.converter import get_rate
import dateutil.relativedelta
import math
def passedPriceFX(c1, c2, window):
    arr = []
    currentTime = datetime.now()
    l = list(str(currentTime))
    tdate = "".join(l[:10])
    d = datetime.strptime(tdate, "%Y-%m-%d")
    i = window
    while i > 0:
            
        d2 = d - dateutil.relativedelta.relativedelta(days=i)
        price = get_rate(c1, c2, d2.date())
        arr.append(price)
        i-=1
    
    print(arr)
    return sum(arr) / len(arr)
