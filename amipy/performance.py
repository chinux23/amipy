from amipy.strategy import Strategy
import os
import pandas as pd
import pkg_resources

class SymbolConfigurations:

    @classmethod
    def load(cls):
        filepath = pkg_resources.resource_filename("amipy", "Resources/Symbol.xlsx")
        return pd.read_excel(filepath, "Basic").set_index("Symbol")

class Performance:
    
    """
    Performance receives a strategy and then calculate its return.
    """

    def __init__(self, id, name, symbol, interval, trades):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.interval = interval
        self.trades = trades

    @classmethod
    def load(cls, path):
        """
        :param path: the path to the csv
        """
        trades = pd.read_csv(path, index_col="Date", parse_dates=True)
        id, symbol, interval = os.path.split(path)[-1].split(".")[0].split("_")

        trades = trades[["Trade", "Price", "Ex. date", "Ex. Price", "Profit"]]

        return cls(id, "default", symbol, interval, trades)

    def isEmpty(self):
        return len(self.trades) == 0

    def __str__(self):
        return "{}_{}_{}".format(self.id, self.symbol, self.interval)


class PerformancePool:

    """
    Performance pool contains a list of performance
    """

    @classmethod
    def load(cls, path):
        """
        :param path: folder path contains all performance files
        """
        files = os.listdir(path)
        files = [file for file in files if file.split(".")[-1] == "csv"]
        performances = [ Performance.load(os.path.join(path, file)) for file in files ]
        return performances



    