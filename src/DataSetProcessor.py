from src.DataPoint import DataPoint
from src.DataSeries import DataSeries
from src.DataSet import DataSet
from src.DataSet import DataSetType
from src.Plotting import PlotTypes
from src.Plotting import Plotting
from src.Networking import Networking
from src.DataSetCalculator import DataSetCalculator
from src.DirectoryManager import DirectoryManager
from src.Csving import Csving
from src.Logger import log


import os
import shutil
import skrf
import plotly.express
from typing import List


class DataSetProcessor:

    scanName = False

    def __init__(self, scanName, dirManager: DirectoryManager):
        self.scanName = scanName
        self.dirManager = dirManager
        self.plotting = Plotting(scanName)
        self.networking = Networking(scanName)
        self.csving = Csving(scanName)
        self.dsCalc = DataSetCalculator(scanName)


    def toNetwork(self, dataSet: DataSet, save: bool = False) -> List[skrf.Network]:
        log.info(f"Converting {dataSet} to Network(s)")

        if save: save = self.dirManager.initDir('touchstone')
        networks = self.networking.createNetwork(dataSet, savePath = save)

        return networks


    def toCsv(self, dataSet: DataSet, save: bool = False) -> None:
        log.info(f"Converting {dataSet} to CSV(s)")

        if save: save = self.dirManager.initDir('csv')
        self.csving.createCsv(dataSet, savePath = save)


    def toPlot(self, dataSet: DataSet, plotType: PlotTypes = PlotTypes.LOGMAG, show: bool = False, save: bool = False) -> List[plotly.express.line]:
        log.info(f"Converting {dataSet} to Plots(s)")

        if save: save = self.dirManager.initDir('plot')
        plots = self.plotting.plot(dataSet, plotType, show = show, savePath = save)

        return plots


    def toOverviewPlot(self, peakSet: DataSet, fullSeries: DataSeries, cutoff, plotType: PlotTypes = PlotTypes.LOGMAG, show: bool = False, save: bool = False) -> List[plotly.express.line]:
        log.info(f"Converting {fullSeries} with {peakSet} to Overview Plot")

        if save: save = self.dirManager.initDir('plot')
        overviewPlot = self.plotting.overviewPlot(peakSet, fullSeries, cutoff, plotType, show = show, savePath = save)

        return overviewPlot


    def average(self, dataSet: DataSet, truncate: int = 0) -> DataSet:
        log.info(f"Calculating average of {dataSet} with truncation of {truncate}")

        averageDataSet = self.dsCalc.average(dataSet, truncate)

        return averageDataSet


    def peaks(self, dataSet: DataSet, cutoff: int = -10) -> DataSet:
        log.info(f"Calculating peaks of {dataSet} with a peak cutoff of {cutoff} db")

        peakDataSet = self.dsCalc.peaks(dataSet, cutoff)

        return peakDataSet
