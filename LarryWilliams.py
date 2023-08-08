import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG


class LerryWilliamsStrategy(Strategy):

	def init(self):
		self.donchian = self.I(self.ta_donchaian, self.data)
		self.volume_sma = self.I(self.ta_volume_sma, self.data)
		
		self.entry = None
		self.donchian_middle = None


	def ta_donchaian(self, data):
		return ta.donchian(data.High.s, data.Low.s, lower_length=10, upper_length=15)

	def ta_volume_sma(self, data):
		return ta.sma(data.Volume.s, length=20)

	def buy(self):
		self.donchian_middle = self.donchian[1][-1]
		self.entry = self.data.Close[-1]
		super().buy()

	def sell(self):
		self.donchian_middle = self.donchian[1][-1]
		self.entry = self.data.Close[-1]
		super().sell()

	def next(self):
		donchian_lower_s = self.donchian[0]
		donchian_upper_s = self.donchian[2]
		
		lo_streak = True
		hi_streak = True
		for i in [1]:
			hi = self.data.High[-i]
			lo = self.data.Low[-i]
			donchian_upper = donchian_upper_s[-i]
			donchian_lower = donchian_lower_s[-i]
			hi_streak &= hi >= donchian_upper
			lo_streak &= lo <= donchian_lower

		volume_green = self.data.Close[-1] > self.data.Open[-1]
		volume_red = self.data.Close[-1] < self.data.Open[-1]
		volume_above_sma = self.data.Volume[-1] > self.volume_sma[-1]

		if all((not self.position, hi_streak, volume_green, volume_above_sma)):
			self.buy()

		if all((self.position, self.position.is_long, self.entry, self.donchian_middle)):
			close = self.data.Close[-1]

			risk = self.entry - self.donchian_middle * (1 - 0.05)
			reward = 2 * risk

			take_profit = self.entry + reward
			stop_loss = self.entry - risk

			if close > take_profit or close < stop_loss:
				self.position.close()
				self.entry = self.donchian_middle = None

		if all((not self.position, lo_streak, volume_red, volume_above_sma)):
			self.sell()

		if all((self.position, self.position.is_short, self.entry, self.donchian_middle)):
			close = self.data.Close[-1]

			risk = self.donchian_middle * (1 + 0.05) - self.entry
			reward = 2 * risk

			take_profit = self.entry - reward
			stop_loss = self.entry + risk

			if close < take_profit or close > stop_loss:
				self.position.close()
				self.entry = self.donchian_middle = None


bt = Backtest(GOOG, LerryWilliamsStrategy, cash=10_000)
stats = bt.run()

print(stats)
