from src.DataPoint import DataPoint
from src.DataSeries import DataSeries
from src.DataSet import DataSet
from src.DataSet import DataSetType
from src.Logger import log


class DataSetCalculator:


    def __init__(self, scanName):
        self.scanName = scanName


    def average(self, dataSet: DataSet, truncate: int = 0) -> DataSet:
        freqs = []
        sMeans = []

        for i in range(dataSet.getDataSeries().length()):

            sVals = []
            for s in dataSet:
                dp = s.getDataPoint(i)
                freq = dp.frequency
                sVal = dp.sReal + dp.sImaginary * 1j
                sVals.append(sVal)

            for t in range(truncate):
                sVals.remove(min(sVals, key=abs))
                sVals.remove(max(sVals, key=abs))

            freqs.append(freq)
            sMeans.append(sum(sVals) / len(sVals))


        meanDataSeries = DataSeries(f"{self.scanName}_average")
        for j in range(len(freqs)):
            meanDataSeries.addDataPoint(DataPoint(freqs[j], sMeans[j].real, sMeans[j].imag))

        meanDataSet = DataSet(self.scanName, DataSetType.AVERAGE)
        meanDataSet.addDataSeries(meanDataSeries)

        return meanDataSet


    def peaks(self, dataSet: DataSet, cutoff: int = -10) -> DataSet:

        if dataSet.length() == 1: inSeries = dataSet.getDataSeries()
        else: inSeries = self.average(dataSet).getDataSeries()

        peaks = self.getPeaks(inSeries, cutoff)

        peakDataSet = DataSet(self.scanName, DataSetType.PEAK)

        for i in range(len(peaks)):
            peakSeries = DataSeries(f"{self.scanName}_peak_{i+1}")

            for k in range(len(peaks[i][0])):
                freq = peaks[i][0][k]
                sReal = peaks[i][1][k].real
                sImag = peaks[i][1][k].imag
                peakSeries.addDataPoint(DataPoint(freq, sReal, sImag))

            peakDataSet.addDataSeries(peakSeries)

        return peakDataSet


    def getPeaks(self, series: DataSeries, cutoff: int):
        peaks = []

        i = 0
        lastI = 0

        for j in range(series.length()):
            dp = series.getDataPoint(j)

            freq = dp.frequency
            sVal = dp.sval
            logmag = dp.logmag

            if logmag <= cutoff:
                if lastI != i - 1:
                    freqs = []
                    sVals = []

                    prevDp = series.getDataPoint(j-1)
                    freqs.append(prevDp.frequency)
                    sVals.append(prevDp.sval)

                freqs.append(freq)
                sVals.append(sVal)

                nextDp = series.getDataPoint(j+1)

                if nextDp == False:
                    peaks.append([freqs, sVals])
                    break

                if nextDp.logmag > cutoff:
                    freqs.append(nextDp.frequency)
                    sVals.append(nextDp.sval)

                    peaks.append([freqs, sVals])


                lastI = i

            i += 1

        return peaks
