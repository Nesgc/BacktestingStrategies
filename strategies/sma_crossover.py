from backtesting import Strategy
from backtesting.lib import crossover
import numpy as np

class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.sma1 = self.I(lambda x: x.rolling(10).mean(), price)
        self.sma2 = self.I(lambda x: x.rolling(20).mean(), price)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()
