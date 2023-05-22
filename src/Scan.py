
from src.ScanData import ScanData
from src.Settings import settings

import time

class Scan:

    vna = False
    start = False
    stop = False
    points = False


    def __init__(self, vna, start, stop, points):
        self.vna = vna
        self.start = start
        self.stop = stop
        self.points = points


    def run(self):
        self.vna.write(f"scan {self.start} {self.stop} {self.points}\r")

        time.sleep(float(settings.get('scanning', 'readDelay')))

        self.vna.write("frequencies\r")
        freqs = self.vna.read()

        self.vna.write("data\r")
        data = self.vna.read()

        return ScanData((freqs, data))
