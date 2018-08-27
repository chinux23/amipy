from win32com.client import Dispatch
import os
import logging
import re
from amipy.strategy import AmibrokerStrategy
import time


class Amibroker:
    """
    Interaction with Amibroker softare to automate theorectical daily returns.
    """

    def __init__(self):
        self.ab = None

    def load_application(self):
        self.ab = Dispatch("Broker.Application")
        self.ab.Visible = False

    def isLoaded(self):
        return self.ab is not None

    def load_database(self, databasePath):
        """
        load amibroker database incase it's different than default.

        :param databasePath: the path to the amibroker database.
        """

        if not self.ab:
            raise Exception("Load Amibroker application first.")

        if not os.path.exists(databasePath):
            raise Exception("database folder can not be found.")

        if self.ab.LoadDatabase(databasePath):
            logging.info("database loaded successfully.")
        else:
            logging.error("failed to load database.")

    def scan_afl(self, path, regularexpression=None):
        if not os.path.exists(path):
            raise Exception("{} not found.".format(path))

        files = []
        for dirName, _, fileList in os.walk(path):
            for file in fileList:
                files.append((dirName, file))

        if regularexpression:
            files = [ file for file in files if regularexpression.match(file[1]) ]

        return files

    def scan_strategies(self, path):
        """
        return a list of strategy objects.
        """

        pattern = re.compile(r"\d+_[a-zA-Z]+_\d+_[a-zA-Z]+_\d+.afl$")
        files = self.scan_afl(path, regularexpression=pattern)
        
        strategies = []

        for file in files:
            path, filename = file
            path = os.path.join(path, filename)
            s_id, s_product, s_period, s_name, _ = filename.split("_")
            strategy_obj = AmibrokerStrategy(s_name, s_id, s_product, s_period, path)
            strategies.append(strategy_obj)

        return strategies

    def backtest(self, strategy, resultfile):
        self.ab.Documents.close()
        self.ab.Documents.open(strategy.symbol)
        
        assert strategy.destination, "You should generate the apx before running backtest."

        analysis = self.ab.AnalysisDocs.Open(strategy.destination)
        if analysis:
            analysis.Run(3)

            while analysis.IsBusy:
                time.sleep( 0.5 )

            analysis.Export( resultfile )
            analysis.Close()

        self.ab.Documents.close()



if __name__ == "__main__":
    pass