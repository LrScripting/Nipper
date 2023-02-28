def maDX(data, window):
   return (data[-1] - data[-1-window]) / window
