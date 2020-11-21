import numpy as np


class PortfolioReturn:

    def __init__(self, portfolio, portfolio_returns):
        portfolio_returns.sort()
        self.mean = np.mean(portfolio_returns)
        self.std_dev = np.std(portfolio_returns)
        self.percentiles = np.percentile(portfolio_returns, range(0, 100, 10))
        self.quantiles = np.percentile(portfolio_returns, range(0, 100, 25))
        self.cvar90 = np.percentile(portfolio_returns, 10)
        self.portfolio = portfolio

    def __str__(self):
        return '{0} with mean {1:.2f} std {2:.2f} cvar90 {3:.2f}'\
              .format(self.portfolio, self.mean, self.std_dev, self.cvar90)

    def __repr__(self):
        return self.__str__()
