class Asset:

    def __init__(self, name, category, mean, std_dev=None, iqr_top=None, iqr_low=None):
        self.name = name
        self.category = category
        self.mean = mean
        if std_dev is not None:
            self.std_dev = std_dev
        if iqr_top is not None and iqr_low is not None:
            iqr = iqr_top - iqr_low
            self.std_dev = self.std_dev = iqr / 1.35
        if self.std_dev is None:
            self.std_dev = 0
