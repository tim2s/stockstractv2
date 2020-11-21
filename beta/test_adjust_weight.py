from unittest import TestCase

from beta.genetic import adjust_weight
from beta.market import MARKET


class TestGenetic(TestCase):

    def test_adjust_weight_incomplete(self):
        incomplete_portfolio = {
            MARKET.gold: 0.2,
            MARKET.us_stocks: 0.15,
            MARKET.real_estate: 0.15
        }

        fixed_portfolio = adjust_weight(incomplete_portfolio)
        self.assertAlmostEquals(1.0, sum(fixed_portfolio.values()))
        self.assertAlmostEquals(0.4, fixed_portfolio.get(MARKET.gold))
        self.assertAlmostEquals(0.3, fixed_portfolio.get(MARKET.real_estate))
        self.assertAlmostEquals(0.3, fixed_portfolio.get(MARKET.us_stocks))
        self.assertIsNone(fixed_portfolio.get(MARKET.eu_stocks))

    def test_adjust_weight_overfull(self):
        overfull_portfolio = {
            MARKET.gold: 0.5,
            MARKET.real_estate: 0.5,
            MARKET.us_stocks: 1.0
        }

        fixed_portfolio = adjust_weight(overfull_portfolio)
        self.assertAlmostEquals(1.0, sum(fixed_portfolio.values()))
        self.assertAlmostEquals(0.25, fixed_portfolio.get(MARKET.gold))
        self.assertAlmostEquals(0.25, fixed_portfolio.get(MARKET.real_estate))
        self.assertAlmostEquals(0.5, fixed_portfolio.get(MARKET.us_stocks))
        self.assertIsNone(fixed_portfolio.get(MARKET.eu_stocks))

