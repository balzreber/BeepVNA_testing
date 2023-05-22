
from src.DataPoint import DataPoint
from src.Logger import log

class ScanData:

    rawData = False
    data = False


    def __init__(self, rawData):
        self.rawData = rawData

        freqData = self.processFreqData(self.rawData[0])
        sData = self.processSData(self.rawData[1])

        if len(freqData) == len(sData):
            self.data = self.generateDataPoints(freqData, sData)
        else:
            log.error(f"Length of Frequency data ({len(freqData)}) and S data ({len(sData)}) do not mach")
            self.data = []


    def processFreqData(self, freqData):
        freqArray = []

        if " " in freqData or "." in freqData:
            log.error("Unexpected Freqency data: spaces or dots found")
            return []

        for line in freqData.split('\n'):
            if line:
                try: f = int(line)
                except Exception as e:
                    log.error("Error appending Frequency: " + str(e))
                    return []

                freqArray.append(int(line))

        return freqArray


    def processSData(self, sData):
        line = False
        outData = []

        for line in sData.split('\n'):
            if line:
                d = line.strip().split(' ')

                try: sR = float(d[0])
                except Exception as e:
                    log.error("Error appending sData (Real): " + str(e))
                    return []

                try: sI = float(d[1])
                except Exception as e:
                    log.error("Error appending sData (Imaginary): " + str(e))
                    return []

                if sR > 100 or sR < -100:
                    log.error("Unexpectedly low/high sData (Real): " + str(sR))
                    return []

                outData.append((sR, sI))

        return outData


    def generateDataPoints(self, freqs, sVals):

        dataPointArray = []

        for i in range(len(freqs)):

            dataPointArray.append(DataPoint(freqs[i], sVals[i][0], sVals[i][1]))

        return dataPointArray


    def get(self):
        return self.data


    def getFirst(self):
        if(len(self.data) == 0): return False
        return self.data[0]


    def getLast(self):
        if(len(self.data) == 0): return False
        return self.data[-1]


    def length(self):
        return len(self.data)
