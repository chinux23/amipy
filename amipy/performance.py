from amipy.strategy import Strategy
import os
import pandas as pd
import pkg_resources
import pytz
import numpy as np


LEVERAGE = 5


class SymbolConfigurations:

    def __init__(self, exchanges, symbols, basic):
        self.exchanges = exchanges
        self.symbols = symbols
        self.basic = basic

    @classmethod
    def load(cls):
        filepath = pkg_resources.resource_filename("amipy", "Resources/Symbol.xlsx")
        exchanges = pd.read_excel(filepath, "Exchange").set_index("exchange")
        exchanges.index = [symbol.strip() for symbol in exchanges.index]
        symbols = pd.read_excel(filepath, "Symbol").set_index("symbol")
        symbols.index = [symbol.strip() for symbol in symbols.index]
        basic = pd.read_excel(filepath, "Basic").set_index("Symbol")
        basic.index = [symbol.strip() for symbol in basic.index]
        return cls(exchanges, symbols, basic)

    def timezone(self, symbol):
        return pytz.timezone(self.exchanges.loc[symbol][0])

    def monetary_base(self, symbol):
        """
        Calculate the monetary value of the contract.
        """
        pass


class Performance:

    """
    Performance receives a strategy and then calculate its return.
    """

    def __init__(self, id, name, symbol, period, pnl):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.interval = period
        self.pnl = pnl["return"].fillna(0)

    @classmethod
    def load(cls, path):
        """
        :param path: the path to the csv
        """
        pnl = pd.read_csv(path, index_col="datetime", parse_dates=True)
        path, filename = os.path.split(path)
        filename, ext = os.path.splitext(filename)
        s_ID, s_Symbol, s_Period, s_Name, _ = filename.split("_")[:5]

        return cls(s_ID, s_Name, s_Symbol, s_Period, pnl)

    def __str__(self):
        return "{}_{}_{}".format(self.id, self.symbol, self.interval)

    def apply_timezone(self):
        configuration = SymbolConfigurations.load()
        exchage = configuration.symbols.loc[self.symbol][0]
        timezone = configuration.exchanges.loc[exchage][0]
        timezone = pytz.timezone(timezone)
        self.pnl = self.pnl.tz_localize(timezone)

    def sharpe_ratio(self):
        returns = self.pnl
        return returns.mean() / returns.std() * np.sqrt(252)

    def expected_return(self):
        return self.pnl.mean()


class Intermediate (Performance):
    """
    This class works as an intermediate step towards our final goal.
    """

    def __init__(self, id, name, symbol, period, pnl):
        Performance.__init__(self, id, name, symbol, period, pnl)

    @classmethod
    def load(cls, path, start_date=None):
        """
        Use the pnls provided and use close data
        """
        results = []
        skipped = []
        closes = cls.load_daily()
        configs = SymbolConfigurations.load()
        pnls = pd.read_csv(path, parse_dates=True, index_col=0)
        for key in pnls:
            try:
                print("Processing strategy: {}".format(key))
                id, symbol, period, name = key.split("_")[:4]
                multipoint = configs.basic["MultiPioint"].loc[symbol]
                close = closes[symbol.lower()]
                new_dataframe = pd.concat([pnls[key], close * multipoint * 1.0 / LEVERAGE], join="inner", axis=1)
                new_dataframe.columns = ["pnl", "base"]
                new_dataframe["return"] = new_dataframe["pnl"] / new_dataframe["base"]
                if start_date:
                    new_dataframe = new_dataframe[start_date:]
                results.append(cls(id, name, symbol, period, new_dataframe))
            except Exception as e:
                print(e)
                skipped.append(key)

        print("The following strategies are skipped due to exception in processing: ")
        print("\t{}".format(skipped))
        return results

    @classmethod
    def load_daily(cls):
        print("Loading daily data. This might take a while.")

        hsi = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/11191001_HSI_1m_OpenFollow_0916_0929_20180523.csv", parse_dates=True, index_col=0)
        hsi = hsi["close"].resample("1D").first()
        hhi = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/11291804_HHI.HK_01_FollowOpen_20180712.csv", parse_dates=True, index_col=0)
        hhi = hhi["close"].resample("1D").first()
        xina50 = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/21191201_XINA50_01_FollowClose1630_20180702.csv", parse_dates=True, index_col=0)
        xina50 = xina50["close"].resample("1D").first()
        nifty = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/21291201_NIFTY_01_FollowClose1800_20180702.csv", parse_dates=True, index_col=0)
        nifty = nifty["close"].resample("1D").first()
        sgxnk = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/21391101_SGXNK_1m_OpenRev_0813_0829_20180725.csv", parse_dates=True, index_col=0)
        sgxnk = sgxnk["close"].resample("1D").first()
        nq = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/31191201_NQ_01_FollowClose_20180711.csv", parse_dates=True, index_col=0)
        nq = nq["close"].resample("1D").first()
        es = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/31291201_ES_01_FollowClose_20180711.csv", parse_dates=True, index_col=0)
        es = es["close"].resample("1D").first()
        cl = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/41191201_CL_15_FollowCloseInner0230_20180724.csv", parse_dates=True, index_col=0)
        cl = cl["close"].resample("1D").first()
        hg = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/51191701_HG_15_ReverseClose_20180730.csv", parse_dates=True, index_col=0)
        hg = hg["close"].resample("1D").first()
        si = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/51391201_SI_15_FollowOpen_20180730.csv", parse_dates=True, index_col=0)
        si = si["close"].resample("1D").first()
        zc = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/61191801_ZC_15_FollowOpen_20180730.csv", parse_dates=True, index_col=0)
        zc = zc["close"].resample("1D").first()
        dax = pd.read_csv("/Volumes/Passport/Repository/Trading/amipy/OtherDocuments/02.Pnl/71191205_DAX_15_FollowClose1945_0145_20180805.csv", parse_dates=True, index_col=0)
        dax = dax["close"].resample("1D").first()

        return {
            "hsi": hsi,
            "hhi.hk": hhi,
            "xina50": xina50,
            "nifty": nifty,
            "sgxnk": sgxnk,
            "nq": nq,
            "es": es,
            "cl": cl,
            "hg": hg,
            "si": si,
            "zc": zc,
            "dax": dax
        }


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
        performances = [Performance.load(os.path.join(path, file)) for file in files]
        for performance in performances:
            print(str(performance))
            performance.apply_timezone()
        return performances


class Portfolio:

    def __init__(self, strategies, weights=None):
        assert len(strategies) == len(weights), "size mismatch between number of strategies and weights"

        self.strategies = strategies
        self.combined = self._combine()
        self._covariance = None

        # The following
        if weights is not None: self.weights = self.normalize(weights)
        else: self.weights = None
        self._variance = None
        self._covariance = None

    def expected_return(self, weights=None):
        if weights is not None:
            weights = self.normalize(weights)
            return np.dot(np.array(weights), self.combined.mean())
        else:
            return np.dot(np.array(self.weights), self.combined.mean())

    def sharpe_ratio(self, weights=None):
        return self.expected_return(weights) / np.sqrt(self.variance(weights)) * np.sqrt(252)

    def variance(self, weights=None):
        return self._variance_impl(weights)

    def _variance_impl(self, weights=None):
        weights = self.normalize(weights) if weights is not None else self.weights
        var = weights.dot(self.covariance).dot(weights.transpose())
        self._variance = var
        return var

    def normalize(self, weights):
        return np.array(weights) * 1.0 / sum(weights)

    @property
    def covariance(self):
        if self._covariance is None:
            self._covariance = self.combined.cov().values
        return self._covariance

    def _combine(self):
        pnls = [performance.pnl for performance in self.strategies]
        names = [performance.id for performance in self.strategies]

        combined = pd.concat(pnls, axis=1, join="inner")
        combined.columns = names
        return combined

    def metric(self, weights):
        pass

    def get_returns_vect(self):
        return self.get_dataframe().values.T

    def get_dataframe(self):
        pnls = [performance.pnl for performance in self.strategies]
        names = [performance.id for performance in self.strategies]
        # names = [i for i in range(len(pnls))]
        returns_dataframe = pd.concat(pnls, axis=1, keys=names).fillna(0)
        return returns_dataframe
