from amipy.strategy import Strategy
import os
import pandas as pd
import pkg_resources

class SymbolConfigurations:

    def __init__(self, exchanges, symbols, basic):
        self.exchanges = exchanges
        self.symbols = symbols
        self.basic = basic

    @classmethod
    def load(cls):
        filepath = pkg_resources.resource_filename("amipy", "Resources/Symbol.xlsx")
        exchanges = pd.read_excel(filepath, "Basic").set_index("Exchange")
        symbols = pd.read_excel(filepath, "Symbol").set_index("symbol")
        basic = pd.read_excel(filepath, "basic").set_index("Symbol")
        return cls(exchanges, symbols, basic)


class Performance:
    
    """
    Performance receives a strategy and then calculate its return.
    """

    def __init__(self, id, name, symbol, period, pnl):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.interval = interval
        self.pnl = pnl

    @classmethod
    def load(cls, path):
        """
        :param path: the path to the csv
        """
        pnl = pd.read_csv(path, index_col="datetime", parse_dates=True)
        path, filename = os.path.split(path)
        filename, ext = os.path.splitext(filename)
        s_ID, s_Symbol, s_Period, s_Name, _ = filename.split("_")

        return cls(s_ID, s_Name, s_Symbol, s_Period, pnl)

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



    