import numpy as np

from beta.asset import Asset
from beta.portfolio_return import PortfolioReturn


class Market:

    def __init__(self):
        self.eu_stocks = Asset(name='EU Equity', category='Equity', mean=5.1, iqr_low=-0.5, iqr_top=11)
        self.us_stocks = Asset(name='US Equity', category='Equity', mean=4.3, iqr_low=-0.3, iqr_top=9.3)
        self.ch_stocks = Asset(name='CH Equity', category='Equity', mean=6.2, iqr_low=-2.8, iqr_top=16.2)
        self.agg_bonds = Asset(name='Global Bonds', category='Bonds', mean=0.8, std_dev=1.8)
        self.real_estate = Asset(name='Real Estate Funds', category='Real Estate', mean=2.0, std_dev=2.0)
        self.cash = Asset(name='Cash', category='Bonds', mean=0, std_dev=0)
        self.gold = Asset(name='Gold', category='Commodity', mean=3.9, std_dev=13.4)
        # todo: add china govt bonds
        # todo: add em equity

        self.assets = [self.eu_stocks,
                       self.us_stocks,
                       self.ch_stocks,
                       self.agg_bonds,
                       self.gold,
                       self.cash,
                       self.real_estate]

        self.market_returns = self.compute_market_returns()

    def evaluate_portfolio_return(self, portfolio):
        portfolio_returns = []
        for value_index in range(0, len(list(self.market_returns.values())[0])):
            value_result = 0
            for asset in portfolio.asset_and_weights.keys():
                value_result += self.market_returns[asset][value_index] * portfolio.weight(asset)
            portfolio_returns.append(value_result)
        return PortfolioReturn(portfolio, portfolio_returns)

    def compute_market_returns(self):
        print('Pre computing market returns for {0} assets'.format(len(self.assets)))
        mean = [asset.mean for asset in self.assets]
        cov = self.get_cov_matrix()
        asset_returns = np.random.default_rng().multivariate_normal(mean, cov, 10000)
        market_returns = {}
        for asset_index in range(0, len(self.assets)):
            market_returns[self.assets[asset_index]] = [values[asset_index] for values in asset_returns]

        print('Finished pre computing')
        return market_returns

    def get_cov_matrix(self):
        return [[self.get_cov(row, column) for column in self.assets] for row in self.assets]

    def get_cov(self, first, second):
        cor = self.get_cor(first, second)
        return first.std_dev * second.std_dev * cor

    def get_assets(self):
        return self.assets

    def get_cor(self, first, second):
        if first.name == second.name:
            return 1

        correlations = {
            (self.real_estate, self.cash): 0,
            (self.real_estate, self.eu_stocks): 0.2,    # made up
            (self.real_estate, self.ch_stocks): 0.2,
            (self.real_estate, self.us_stocks): 0.2,
            (self.real_estate, self.agg_bonds): -0.35,  # made up
            (self.agg_bonds, self.eu_stocks): -0.11,
            (self.agg_bonds, self.ch_stocks): -0.2,
            (self.agg_bonds, self.us_stocks): -0.32,
            (self.agg_bonds, self.cash): 0,
            (self.eu_stocks, self.cash): 0,
            (self.eu_stocks, self.ch_stocks): 0.44,
            (self.eu_stocks, self.us_stocks): 0.82,
            (self.ch_stocks, self.cash): 0,
            (self.ch_stocks, self.us_stocks): 0.52,
            (self.us_stocks, self.cash): 0,
            (self.gold, self.eu_stocks): 0.12,
            (self.gold, self.ch_stocks): 0.12,
            (self.gold, self.us_stocks): -0.06,
            (self.gold, self.real_estate): 0.3,         # made up
            (self.gold, self.cash): -0.17,
            (self.gold, self.agg_bonds): 0.14,
        }
        by_key = correlations.get((first, second))
        if by_key is not None:
            return by_key

        by_reverse = correlations.get((second, first))
        assert by_reverse is not None, 'Could not find correlation for %s, %s' % (first.name, second.name)
        return by_reverse


MARKET = Market()
