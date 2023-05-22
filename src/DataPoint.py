
import math

class DataPoint:

    sval = False
    amp = False
    vswr = False
    logmag = False


    def __init__(self, frequency, sReal, sImaginary):
        self.frequency = frequency
        self.sReal = sReal
        self.sImaginary = sImaginary
        self.sval = self.calcSval()


    def calcSval(self):
        return self.sReal + self.sImaginary * 1j

    def calcAmp(self):
        self.amp = math.sqrt(self.sReal ** 2 + self.sImaginary ** 2)

    def calcVswr(self):
        if not self.amp: self.calcAmp()
        self.vswr = (1 + self.amp) / (1 - self.amp)

    def calcLogmag(self):
        if not self.amp: self.calcAmp()
        self.logmag = 20 * math.log(self.amp)

    def __repr__(self):
        return f"<src.DataPoint Object with Freq: {self.frequency/1e6} MHz, sReal: {self.sReal} and sImaginary: {self.sImaginary}>"
