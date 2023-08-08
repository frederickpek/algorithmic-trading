from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG, SMA


class SmaStrategy(Strategy):

    '''
    Long only SMA strategy.
    Long when shorter SMA rises above longer SMA, indicating bullush momentum.
    Close long position when longer SMA rises above shorter SMA, indicating bearish momentum. 
    '''

    sma_lo_lookback_period = 20
    sma_hi_lookback_period = 50

    def init(self):
        self.sma_lo = self.I(SMA, self.data.Close, self.sma_lo_lookback_period)
        self.sma_hi = self.I(SMA, self.data.Close, self.sma_hi_lookback_period)

    def next(self):
        if crossover(self.sma_lo, self.sma_hi):
            if not self.position:
                self.buy()
        elif crossover(self.sma_hi, self.sma_lo):
            if self.position:
                self.position.close()


bt = Backtest(GOOG, SmaStrategy, cash=10_000)
stats = bt.run()

print(stats)
