from src.VNA import VNA
from src.Scan import Scan
from src.DataSeries import DataSeries
from src.DataSet import DataSet
from src.DataSet import DataSetType
from src.Logger import log
from src.Settings import settings

import math

class Scanner:

    vna = False


    def __init__(self, vna: VNA, scanName: str) -> None:
        self.vna = vna
        self.scanName = scanName


    def scan(self, name: str, start: int, stop: int, points: int = 0, step: int = 0, runs: int = 1) -> DataSet:

        log.info("Scan initiated with the following parameters:")

        if (points == 0 and step == 0) or (points != 0 and step != 0):
            log.critical("scan in scanner requires points or steps and not both")
            exit()

        elif points != 0:
            log.info(f"Name: {name} / Start: {start/1e6} MHz / Stop: {stop/1e6} MHz / Points: {points} / Runs: {runs}")
            frequencies = self.getFreqFromPoints(start, stop, points)

        elif step != 0:
            log.info(f"Name: {name} / Start: {start/1e6} MHz / Stop: {stop/1e6} MHz / Step: {step/1e6} MHz / Runs: {runs}")
            frequencies = self.getFreqFromSteps(start, stop, step)

        scans = DataSet(self.scanName, DataSetType.SCAN)
        for r in range(runs):
            scans.addDataSeries(self.execScan(frequencies, r, runs))
            log.info(f"Run {r+1} of {runs} sucessfully completed")

        return scans


    def getFreqFromPoints(self, start: int, stop: int, points: int) -> list:
        frequencies = self.linspace(start, stop, points)

        return frequencies


    def getFreqFromSteps(self, start: int, stop: int, step: int) -> list:
        newStop = stop + start
        points = math.ceil((stop - start) / step) + 1
        frequencies = self.linspace(start, newStop, points)

        return frequencies


    def linspace(self, start: int, stop: int, points: int) -> list:
        delta = (stop-start)/(points-1)
        linspace = [start + i * delta for i in range(points)]

        return linspace


    def execScan(self, frequencies: list, runNr: int, runTotal: int) -> DataSeries:
        segmentLength = 101
        consecutiveErrors = 0

        if runTotal == 1: dataSeriesName = self.scanName
        elif runTotal > 1: dataSeriesName = f"{self.scanName}_{runNr+1}"
        dataSeries = DataSeries(dataSeriesName)

        while len(frequencies) > 0:
            segmentStart = frequencies[0]

            if len(frequencies) >= segmentLength: segmentStop = frequencies[segmentLength-1]
            else: segmentStop = frequencies[-1]

            if len(frequencies) >= segmentLength: length = segmentLength
            else: length = len(frequencies)

            log.info(f"Run {runNr+1} of {runTotal}. Scanning {str(length)} points from: {str(segmentStart / 1e6)} MHz to {str(segmentStop / 1e6)} MHz")

            scan = Scan(self.vna, segmentStart, segmentStop, length)
            scanData = scan.run()

            if scanData.length() != length:
                log.warning(f"Expected {length} Data Points, got {scanData.length()}. Repeating Scan.")
                consecutiveErrors += 1

            elif int(scanData.getFirst().frequency) != int(segmentStart):
                log.warning(f"First Frequency of scan {int(segmentStart) / 1e6} MHz does not mach first Frequency of scan results {int(scanData.getFirst().frequency) / 1e6} MHz. Repeating Scan.")
                consecutiveErrors += 1

            elif int(scanData.getLast().frequency) != int(segmentStop):
                log.warning(f"Last Frequency of scan {int(segmentStop) / 1e6} MHz does not mach last Frequency of scan results {int(scanData.getLast().frequency) / 1e6} MHz. Repeating Scan.")
                consecutiveErrors += 1

            else:
                for sd in scanData.get():
                    dataSeries.addDataPoint(sd)

                frequencies = frequencies[segmentLength:]
                consecutiveErrors = 0

            if consecutiveErrors == int(settings.get('scanning', 'maxConsecutiveErrors')):
                log.critical(f"Got {consecutiveErrors} Scan Errors in a row. Giving up.")
                exit()

        self.vna.resume()

        return dataSeries
