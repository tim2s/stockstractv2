class Portfolio:

    def __init__(self, name, asset_and_weights):
        self.name = name
        self.asset_and_weights = asset_and_weights
        assert sum(self.asset_and_weights.values()) == 1, 'Portfolio weights dont add up : %s' % self.asset_and_weights

    def weight(self, asset):
        return self.asset_and_weights.get(asset, 0)
