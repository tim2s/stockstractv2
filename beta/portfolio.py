import math


class Portfolio:

    def __init__(self, name, asset_and_weights):
        self.name = name
        self.asset_and_weights = asset_and_weights
        assert math.isclose(sum(self.asset_and_weights.values()), 1), 'Portfolio weights dont add up : %s' % self.asset_and_weights

    def weight(self, asset):
        return self.asset_and_weights.get(asset, 0)

    def __str__(self):
        return 'Portfolio {0} with Assets [ {1} ]'.format(self.name, self.print_assets())

    def __repr__(self):
        return self.__str__()

    def print_assets(self):
        return ', '.join([self.print_asset(asset_item) for asset_item in self.asset_and_weights.items()])

    @staticmethod
    def print_asset(asset_item):
        return '{0} : {1:.2f}'.format(asset_item[0], asset_item[1])

