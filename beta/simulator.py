import matplotlib.pyplot as plt
import numpy as np

from beta.market import Market
from beta.portfolio import Portfolio


def evaluate(market, portfolio, asset_return):

    return sum(portfolio.weight(market.get_assets()[asset_index]) * asset_return[asset_index] for asset_index in range(len(market.get_assets())))


def compute():

    market = Market()

    portfolio_0_100 = Portfolio('Pure Bond', {
        market.eu_stocks: 0,
        market.agg_bonds: 1,
        market.gold: 0
    })

    portfolio_40_60 = Portfolio('40/60', {
        market.eu_stocks: 0.4,
        market.agg_bonds: 0.6,
        market.gold: 0
    })

    portfolio_50_50 = Portfolio('50/50', {
        market.eu_stocks: 0.5,
        market.agg_bonds: 0.5,
        market.gold: 0
    })

    portfolio_60_40 = Portfolio('60/40', {
        market.eu_stocks: 0.6,
        market.agg_bonds: 0.4,
        market.gold: 0
    })

    portfolio_70_30 = Portfolio('70/30', {
        market.eu_stocks: 0.7,
        market.agg_bonds: 0.3,
        market.gold: 0
    })

    portfolio_100_0 = Portfolio('Pure Equity', {
        market.eu_stocks: 1,
        market.agg_bonds: 0,
        market.gold: 0
    })

    golden_butterfly = Portfolio('Golden Butterfly', {
        market.eu_stocks: 0.4,
        market.agg_bonds: 0.4,
        market.gold: 0.2
    })

    mine = Portfolio('Custom', {
        market.ch_stocks: 0.25,
        market.eu_stocks: 0.35,
        market.agg_bonds: 0.2,
        market.cash: 0.1,
        market.gold: 0.1
    })

    dalio_curr = Portfolio('Bridgewater', {
        market.eu_stocks: 0.05,
        market.ch_stocks: 0.3,
        market.us_stocks: 0.4,
        market.agg_bonds: 0.05,
        market.gold: 0.2
    })

    portfolios = [portfolio_0_100,
                  # portfolio_40_60,
                  portfolio_50_50,
                  portfolio_60_40,
                  portfolio_70_30,
                  portfolio_100_0,
                  golden_butterfly,
                  mine,
                  dalio_curr]

    mean = [asset.mean for asset in market.get_assets()]

    cov = get_cov_matrix(market)

    asset_returns = np.random.default_rng().multivariate_normal(mean, cov, 50000)

    print(cov, mean)

    all_returns = [[evaluate(market, p, asset_return) for asset_return in asset_returns] for p in portfolios]

    fig = plt.figure()
    ax = fig.add_subplot()
    plt.yticks(range(-20, 20)[::2])
    ax.grid(b=True, which='both', axis='y')
    ax.boxplot(all_returns, sym='')
    ax.set_xticklabels([p.name for p in portfolios])
    plt.show()

    return zip(portfolios, all_returns)


def get_cov_matrix(market):
    return [[get_cov(market, row, column) for column in market.get_assets()] for row in market.get_assets()]


def get_cov(market, first, second):
    cor = market.get_cor(first, second)
    return first.std_dev * second.std_dev * cor