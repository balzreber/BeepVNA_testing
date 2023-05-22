from src.DataSeries import DataSeries
from src.DataSet import DataSet
from src.DataSet import DataSetType

from enum import Enum
import plotly.express
import plotly.graph_objects as plotlyGo
from typing import List

class PlotTypes(Enum):
    SVALS = 1
    AMP = 2
    VSWR = 3
    LOGMAG = 4


class Plotting:

    def __init__(self, scanName):
        self.scanName = scanName


    def getXAxisData(self, dataSeries: DataSeries) -> List[int]:
        xAxisData = []

        for dp in dataSeries:
            xAxisData.append(int(dp.frequency / 1e6))

        return xAxisData


    def getYAxisData(self, dataSeries: DataSeries, plotType: PlotTypes) -> List[float]:
        yAxisData = []

        for dp in dataSeries:

            if plotType is PlotTypes.SVALS:
                yAxisData.append(dp.sReal)
                label = "sVals"

            elif plotType is PlotTypes.AMP:
                dp.calcAmp()
                yAxisData.append(dp.amp)
                label = "Amplitude"

            elif plotType is PlotTypes.VSWR:
                dp.calcVswr()
                yAxisData.append(dp.vswr)
                label = "VSWR"

            elif plotType is PlotTypes.LOGMAG:
                dp.calcLogmag()
                yAxisData.append(dp.logmag)
                label = "LogMag [db]"

        yAxisData.append(label)
        return yAxisData


    def plot(self, dataSet: DataSet, plotType: PlotTypes = PlotTypes.LOGMAG, show: bool = False, savePath: str = False) -> List[plotly.express.line]:
        plots = []

        for dataSeries in dataSet:
            xAxis = self.getXAxisData(dataSeries)
            yAxis = self.getYAxisData(dataSeries, plotType)

            yAxisLabel = yAxis[-1]
            yAxis = yAxis[:-1]

            plot = plotlyGo.Figure()
            plot.add_trace(plotlyGo.Scatter(x = xAxis, y = yAxis, mode = "lines", name = yAxisLabel))
            plot.update_layout(
                title=dataSeries.getName(),
                xaxis_title="Frequency",
                yaxis_title=yAxisLabel,
                font=dict(
                    family="Arial",
                    size=12,
                    color="#000000"
                )
            )

            plots.append(plot)

            if show: plot.show()
            if savePath: plot.write_html(f"{savePath}/{dataSeries.getName()}.html")

        return plots



    def overviewPlot(self, peakSet: DataSet, fullSeries: DataSeries, cutoff: int, plotType: PlotTypes = PlotTypes.LOGMAG, show: bool = False, savePath: str = False) -> plotly.express.line:

        set = DataSet(self.scanName, DataSetType.SCAN)
        set.addDataSeries(fullSeries)

        plots = self.plot(set, plotType)
        plot = plots[0]

        for dataSeries in peakSet:
            firstGraph = dataSeries.getFirst().frequency / 1e6
            firstText = dataSeries.getDataPoint(2).frequency / 1e6
            lastGraph = dataSeries.getLast().frequency / 1e6
            lastText = dataSeries.getDataPoint(-2).frequency / 1e6

            if firstGraph != lastGraph:
                plot.add_vrect(
                    x0=firstGraph, x1=lastGraph,
                    fillcolor="#00FF00", opacity=0.5,
                    layer="below", line_width=0, label=dict(text=f"{firstText} MHz - {lastText} MHz", textposition="bottom left", textangle=-90, padding=20)
                )

        plot.add_hline(y=cutoff, line_width=1, line_dash="dash", line_color="#FF0000", annotation_text=f"Cutoff: {cutoff}db", annotation_position="top left", annotation_font_size=16, annotation_font_color="#000000")
        plot.update_layout(title=f"{self.scanName}_Overview")

        if show: plot.show()
        if savePath: plot.write_html(f"{savePath}/{self.scanName}_overview.html")

        return plot
