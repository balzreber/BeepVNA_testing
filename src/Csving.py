from src.DataSet import DataSet

import csv

class Csving:

    def __init__(self, scanName):
        self.scanName = scanName


    def createCsv(self, dataSet: DataSet, savePath: str = False) -> None:

        for dataSeries in dataSet:

            dataSeries.calcVswrs()
            dataSeries.calcLogmags()

            header = ["Frequency", "S11Real", "S11Imaginary", "LOGMAG", "VSWR"]

            if savePath: filename = f"{savePath}/{dataSeries.getName()}.csv"

            with open(filename, "w", encoding="UTF8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)

                for dp in dataSeries:
                    writer.writerow([dp.frequency, dp.sReal, dp.sImaginary, dp.logmag, dp.vswr])
