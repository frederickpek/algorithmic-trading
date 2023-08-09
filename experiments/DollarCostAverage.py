from backtesting import Backtest, Strategy
from backtesting.test import GOOG

usd_buy_amt = 100

class DcaStrategy(Strategy):

    def init(self):
        self.usd_buy_amt = usd_buy_amt

    def is_monday(self):
        day = self.data.index[-1].day
        return day % 7 == 1

    def next(self):
        close = self.data.Close[-1]
        shares_qty = self.usd_buy_amt // close
        if self.is_monday():
            self.buy(size=shares_qty)


initial_cash = 100_000
bt = Backtest(GOOG * 1e-6, DcaStrategy, cash=initial_cash)
stats = bt.run()
print(stats)

num_trades = stats['# Trades']
equity_invested = num_trades * usd_buy_amt
equity_final = stats['Equity Final [$]']
returns = (equity_final - initial_cash) / equity_invested
print(f'returns: {returns * 100:.2f}%')
