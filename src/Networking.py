from src.DataPoint import DataPoint
from src.DataSet import DataSet
from src.DataSeries import DataSeries

import skrf

class Networking:

    def __init__(self, scanName):
        self.scanName = scanName


    def skrfNetwork(self, frequencies: list[int], sData: list[float]) -> skrf.Network:
        skrfNetwork = skrf.Network()
        skrfNetwork.frequency = skrf.Frequency.from_f(frequencies, unit='hz')
        skrfNetwork.s = (sData)

        return skrfNetwork


    def createNetwork(self, dataSet: DataSet, savePath: str = False) -> list[skrf.Network]:
        networks = []

        for dataSeries in dataSet:
            frequencies = []
            sValues = []

            for dp in dataSeries:
                frequencies.append(dp.frequency)
                sValues.append(dp.sReal + dp.sImaginary * 1.j)

            net = self.skrfNetwork(frequencies, sValues)
            networks.append(net)

            if savePath: net.write_touchstone(f"{savePath}/{dataSeries.getName()}.s1p")

        return networks
