from data.dataManagers.abstracts.fileManager import FileManager
from log.logger import Logger
import csv
import os
import pandas as pd

class CSVManager(FileManager):

    FILE_TYPE: str = "csv"

    def __init__(self, header: list, filename, folderpath: str,) -> None:
        super().__init__(filename, folderpath, self.FILE_TYPE)
        self.logger = Logger(loggerName="CSVManager")
        self.header = header
        if(self._isFileEmpty()):
            self.writeHeader()

    def writeHeader(self) -> None:
        with open(self.absolutPath, "a", encoding="UTF-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.header)

    def writeLine(self, row: list) -> None:
        if (len(row) != len(self.header)):
            self.logger.warn("number of inputs in the row do not match the number of values in the header.")

        with open(self.absolutPath, "a", encoding="UTF-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def readCSV(self) -> pd.DataFrame:
        return pd.read_csv(self.absolutPath)
    
    def _isFileEmpty(self) -> bool:
        return os.path.getsize(self.absolutPath) == 0