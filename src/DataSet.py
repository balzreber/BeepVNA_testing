from src.DataSeries import DataSeries
from src.DataPoint import DataPoint
from src.Logger import log

from enum import Enum

class DataSetType(Enum):
    SCAN = 1
    AVERAGE = 2
    PEAK = 3


class DataSet:

    def __init__(self, scanName: str, type: DataSetType):
        self.scanName = scanName
        self.type = type
        
        self.dataSeries = []
        self.iterIndex = 0


    def addDataSeries(self, dataSeries: DataSeries) -> None:
        self.dataSeries.append(dataSeries)


    def getDataSeries(self, index: int = 0) -> DataSeries:
        return self.dataSeries[index]


    def length(self) -> int:
        return len(self.dataSeries)


    def getType(self) -> DataSetType:
        return self.type


    def __repr__(self) -> str:
        if(self.length() == 0): return f"<src.DataSet Object of type {self.type} containing 0 DataSeries>"
        else: return f"<src.DataSet Object of type {self.type} containing {self.length()} DataSeries>"


    def __iter__(self):
        return self


    def __next__(self):
        if self.iterIndex < self.length():
            iSeries = self.dataSeries[self.iterIndex]
            self.iterIndex += 1
            return iSeries

        self.iterIndex = 0
        raise StopIteration
