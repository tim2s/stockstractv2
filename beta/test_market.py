from unittest import TestCase

from beta.market import MARKET
from beta.portfolio import Portfolio


class TestMarket(TestCase):

    def test_evaluate_portfolio_return(self):

        single_asset_portfolio = Portfolio('US Stocks only', {MARKET.real_estate: 1})

        portfolio_return = MARKET.evaluate_portfolio_return(single_asset_portfolio)

        self.assertAlmostEqual(portfolio_return.mean, MARKET.real_estate.mean, delta=0.5)

    def test_portfolios(self):
        portfolio_0_100 = Portfolio('Pure Bond', {
            MARKET.eu_stocks: 0,
            MARKET.agg_bonds: 1,
            MARKET.gold: 0
        })

        portfolio_50_50 = Portfolio('50/50', {
            MARKET.eu_stocks: 0.5,
            MARKET.agg_bonds: 0.5,
            MARKET.gold: 0
        })

        portfolio_60_40 = Portfolio('60/40', {
            MARKET.eu_stocks: 0.6,
            MARKET.agg_bonds: 0.4,
            MARKET.gold: 0
        })

        portfolio_100_0 = Portfolio('Pure Equity', {
            MARKET.eu_stocks: 1,
            MARKET.agg_bonds: 0,
            MARKET.gold: 0
        })

        golden_butterfly = Portfolio('Golden Butterfly', {
            MARKET.eu_stocks: 0.4,
            MARKET.agg_bonds: 0.4,
            MARKET.gold: 0.2
        })

        varx = Portfolio('VarX', {
            MARKET.ch_stocks: 0.175,
            MARKET.us_stocks: 0.175,
            MARKET.eu_stocks: 0.20,
            MARKET.agg_bonds: 0.15,
            MARKET.real_estate: 0.05,
            MARKET.cash: 0.15,
            MARKET.gold: 0.1
        })

        varx_plus = Portfolio('VarX+', {
            MARKET.ch_stocks:   0.185,
            MARKET.us_stocks:   0.185,
            MARKET.eu_stocks:   0.20,
            MARKET.agg_bonds:   0.15,
            MARKET.real_estate: 0.05,
            MARKET.cash:        0.13,
            MARKET.gold:        0.10
        })

        current = Portfolio('current', {
            MARKET.ch_stocks: 0.055,
            MARKET.us_stocks: 0.12,
            MARKET.eu_stocks: 0.285,
            MARKET.agg_bonds: 0.105,
            MARKET.real_estate: 0.005,
            MARKET.cash: 0.375,
            MARKET.gold: 0.055
        })

        dalio_curr = Portfolio('Bridgewater', {
            MARKET.eu_stocks: 0.05,
            MARKET.ch_stocks: 0.3,
            MARKET.us_stocks: 0.4,
            MARKET.agg_bonds: 0.05,
            MARKET.gold: 0.2
        })

        portfolios = [portfolio_0_100,
                      portfolio_50_50,
                      portfolio_60_40,
                      portfolio_100_0,
                      golden_butterfly,
                      current,
                      varx,
                      varx_plus,
                      dalio_curr]

        for p in portfolios:
            print(MARKET.evaluate_portfolio_return(p))
