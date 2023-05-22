
class DataSeries:

    hasAmps = False
    hasVswrs = False
    hasLogmags = False

    def __init__(self, name):
        self.name = name

        self.points = []
        self.iterIndex = 0


    def addDataPoint(self, point):
        self.points.append(point)


    def getDataPoint(self, index):
        if index < len(self.points): return self.points[index]
        return False


    def getName(self):
        return self.name


    def getFirst(self):
        return self.points[0]


    def getLast(self):
        return self.points[-1]


    def length(self):
        return len(self.points)


    def calAmps(self):
        if not self.hasAmps:
            for p in self.points:
                p.calcAmp()
            self.hasAmps = True


    def calcVswrs(self):
        if not self.hasVswrs:
            for p in self.points:
                p.calcVswr()
            self.hasVswrs = True


    def calcLogmags(self):
        if not self.hasLogmags:
            for p in self.points:
                p.calcLogmag()
            self.hasLogmags = True


    def __repr__(self):
        if(self.length() == 0): return f"<src.DataSeries Object containing 0 Points>"
        else:  return f"<src.DataSeries Object from {self.points[0].frequency/1e6} MHz to {self.points[-1].frequency/1e6} MHz containing {self.length()} Points>"


    def __iter__(self):
        return self


    def __next__(self):
        if self.iterIndex < self.length():
            iPoint = self.points[self.iterIndex]
            self.iterIndex += 1
            return iPoint

        self.iterIndex = 0
        raise StopIteration
