import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG


class BollingerBandsStrategy(Strategy):

	def init(self):
		self.bbands = self.I(self.indicator, self.data)

	def indicator(self, data):
		return ta.bbands(close=data.Close.s, length=20, std=2)

	def next(self):
		close = self.data.Close
		upper_band = self.bbands[2]
		lower_band = self.bbands[0]

		if crossover(lower_band, close):
			if not self.position:
				self.buy()
		elif crossover(close, upper_band):
			if self.position:
				self.position.close()

bt = Backtest(GOOG, BollingerBandsStrategy, cash=10_000)
stats = bt.run()

print(stats)

