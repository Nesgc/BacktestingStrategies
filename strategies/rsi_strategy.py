from backtesting import Strategy
import pandas as pd

def RSI(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

class RsiStrategy(Strategy):
    def init(self):
        self.rsi = self.I(RSI, self.data.Close, 14)

    def next(self):
        if self.rsi[-1] < 30 and not self.position:
            self.buy()
        elif self.rsi[-1] > 70 and self.position:
            self.sell()
