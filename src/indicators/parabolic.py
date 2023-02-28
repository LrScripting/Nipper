def calculateParabolicSAR(high, low, af_start=0.02, af_step=0.02, af_max=0.2):
    af = af_start
    sar = [low[0]]
    if high[1] > high[0]:
        trend = "bullish"
        ep = high[1]
        sar.append(min(low[0], low[1]))
    else:
        trend = "bearish"
        ep = low[1]
        sar.append(max(high[0], high[1]))
    for i in range(2, len(high)):
        if trend == "bullish":
            if high[i] > ep:
                ep = high[i]
                af = min(af + af_step, af_max)
            sar_next = sar[-1] + af * (ep - sar[-1])
            if sar_next > low[i]:
                trend = "bearish"
                ep = low[i]
                af = af_start
                sar_next = sar[-1] + af * (ep - sar[-1])
            sar.append(sar_next)
        else:
            if low[i] < ep:
                ep = low[i]
                af = min(af + af_step, af_max)
            sar_next = sar[-1] + af * (ep - sar[-1])
            if sar_next < high[i]:
                trend = "bullish"
                ep = high[i]
