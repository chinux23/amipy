from win32com.client import Dispatch
import os
import logging
import re


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
        for dirName, subdirList, fileList in os.walk(path):
            for file in fileList:
                files.append((dirName, file))

        if regularexpression:
            files = [ file for file in files if regularexpression.match(file[1]) ]

        return files

if __name__ == "__main__":
    pass