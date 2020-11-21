from random import random

import matplotlib.pyplot as plt
import numpy as np

from beta.market import Market
from beta.portfolio import Portfolio


def evaluate(market, portfolio, asset_return):

    return sum(portfolio.weight(market.get_assets()[asset_index]) * asset_return[asset_index] for asset_index in range(len(market.get_assets())))


def evaluate_portfolio(market, portfolio, asset_returns):
    return [evaluate(market, portfolio, asset_return) for asset_return in asset_returns]


def optimize():

    market = Market()

    asset_returns = compute_market_returns(market)

    min_lower = -10

    valid_portfolios = []

    for i in range(0, 100):
        asset_weights = {}
        left = 1
        for asset in market.get_assets():
            weight = random() * left
            asset_weights[asset] = weight
            left = left - weight

        if left > 0:
            asset_weights[market.get_assets()[:1][0]] += left

        portfolio = Portfolio('Portfolio' + str(i), asset_weights)

        portfolio_returns = evaluate_portfolio(market, portfolio, asset_returns)
        if np.percentile(portfolio_returns, 25) > min_lower:
            valid_portfolios.append((portfolio, portfolio_returns))

    valid_portfolios.sort(key=lambda p: np.mean(p[1]), reverse=True)
    best_portfolio = valid_portfolios[0]
    comparisons = [compute()]
    to_display = comparisons.append(best_portfolio)
    return to_display


def compute():

    market = Market()

    portfolio_0_100 = Portfolio('Pure Bond', {
        market.eu_stocks: 0,
        market.agg_bonds: 1,
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

    varx = Portfolio('VarX', {
        market.ch_stocks: 0.175,
        market.us_stocks: 0.175,
        market.eu_stocks: 0.20,
        market.agg_bonds: 0.15,
        market.real_estate: 0.05,
        market.cash: 0.15,
        market.gold: 0.1
    })

    current = Portfolio('current', {
        market.ch_stocks: 0.055,
        market.us_stocks: 0.12,
        market.eu_stocks: 0.285,
        market.agg_bonds: 0.105,
        market.real_estate: 0.005,
        market.cash: 0.375,
        market.gold: 0.055
    })

    dalio_curr = Portfolio('Bridgewater', {
        market.eu_stocks: 0.05,
        market.ch_stocks: 0.3,
        market.us_stocks: 0.4,
        market.agg_bonds: 0.05,
        market.gold: 0.2
    })

    portfolios = [portfolio_0_100,
                  portfolio_50_50,
                  portfolio_60_40,
                  portfolio_100_0,
                  golden_butterfly,
                  current,
                  varx,
                  dalio_curr]

    asset_returns = compute_market_returns(market)

    all_returns = [evaluate_portfolio(market, p, asset_returns) for p in portfolios]

    fig = plt.figure()
    ax = fig.add_subplot()
    plt.yticks(range(-20, 20)[::2])
    ax.grid(b=True, which='both', axis='y')
    ax.boxplot(all_returns, sym='')
    ax.set_xticklabels([p.name for p in portfolios])
    plt.show()

    return zip(portfolios, all_returns)


def compute_market_returns(market):
    print('Pre computing market returns for ' + str(len(market.get_assets())) + ' assets')
    mean = [asset.mean for asset in market.get_assets()]
    cov = get_cov_matrix(market)
    asset_returns = np.random.default_rng().multivariate_normal(mean, cov, 10000)
    print('Finished pre computing')
    return asset_returns


def get_cov_matrix(market):
    return [[get_cov(market, row, column) for column in market.get_assets()] for row in market.get_assets()]


def get_cov(market, first, second):
    cor = market.get_cor(first, second)
    return first.std_dev * second.std_dev * cor
