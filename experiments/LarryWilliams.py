import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.test import GOOG


class LerryWilliamsStrategy(Strategy):

    '''
    Momentum based breakout strategy by Lerry Williams.
    Uses the Donchian Channels indicator, simple moving average of volume
    and an additional Lerry Williams Large Trade Index indicator that has been omitted here.

    Donchian Channels generally used similarly to bbands, but used here to find breakout points.
    LTI is a long/short term trend indicator used to affirm breakout.
    Volume SMA used to indicate non-consolidating market.

    Avoid:
        Note to avoid longs near major resistance levels,
        and avoid shorts near major support levels on higher time frame.
        Unless the close breaks pasts these levels.

        Do not set stop-loss at donchian middle band when upper/lower band deviates
        too far from it. Instead, set stop-loss at recent swing high/low.

        Omitted here.

    Strategy:
        Enter long when the following conditions are all met
            - close consecutively hits upper band
            - volume indicator is green (close > open)
            - volume is above the volume SMA
            - LTI is green (?).
        Similar conditions applies for shorts.
    '''

    def init(self):
        self.donchian = self.I(self.ta_donchian, self.data)
        self.volume_sma = self.I(self.ta_volume_sma, self.data)
        
        self.entry = None
        self.donchian_middle = None

    def ta_donchian(self, data):
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
        
        lo_streak = hi_streak = True
        streaks_required = 1
        for i in range(1, streaks_required + 1, 1):
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
