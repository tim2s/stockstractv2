from beta.asset import Asset


class Market:

    def __init__(self):
        self.eu_stocks = Asset(name='EU Stocks', category='Equity', mean=5.1, iqr_low=-0.5, iqr_top=11)
        self.us_stocks = Asset(name='US Stocks', category='Equity', mean=4.3, iqr_low=-0.3, iqr_top=9.3)
        self.ch_stocks = Asset(name='CH Stocks', category='Equity', mean=6.2, iqr_low=-2.8, iqr_top=16.2)
        self.agg_bonds = Asset(name='Agg Bonds', category='Bonds', mean=-1.1, iqr_low=-2.2, iqr_top=0)
        self.cash = Asset(name='Cash', category='Bonds', mean=0, std_dev=0)
        self.gold = Asset(name='Gold', category='Commodity', mean=3.9, std_dev=13.4)
        # todo: add china govt bonds
        # todo: add em equity

    def get_assets(self):

        assets = [self.eu_stocks, self.agg_bonds, self.gold, self.cash]

        return assets

    def get_cor(self, first, second):
        if first.name == second.name:
            return 1

        correlations = {
            (self.agg_bonds, self.eu_stocks): -0.11,
            (self.agg_bonds, self.ch_stocks): -0.2,
            (self.agg_bonds, self.us_stocks): -0.32,
            (self.agg_bonds, self.cash): 0,
            (self.eu_stocks, self.cash): 0,
            (self.eu_stocks, self.ch_stocks): 0.44,
            (self.eu_stocks, self.us_stocks): 0.82,
            (self.ch_stocks, self.cash): 0,
            (self.us_stocks, self.cash): 0,
            (self.gold, self.eu_stocks): 0.12,
            (self.gold, self.ch_stocks): 0.12,
            (self.gold, self.us_stocks): -0.06,
            (self.gold, self.cash): -0.17,
            (self.gold, self.agg_bonds): 0.14,
        }
        by_key = correlations.get((first, second))
        if by_key is not None:
            return by_key

        by_reverse = correlations.get((second, first))
        assert by_reverse is not None, 'Could not find correlation for %s, %s' % (first.name, second.name)
        return by_reverse
