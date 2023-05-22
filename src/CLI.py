
import sys
import re
from optparse import OptionParser
from src.Logger import log
from src.Settings import settings

class CLI:

    def __init__(self) -> None:
        self.parser = OptionParser(usage="%prog: [options] or -? for help")
        self.addOptions()

        cliString = ' '.join(sys.argv[1:])
        log.info(f"Input arguments: {cliString}")

        (self.opt, self.args) = self.parser.parse_args()
        self.verifyArgs(self.opt, self.args)


    def addOptions(self) -> None:
        self.parser.add_option("-n", "--name", dest="name", help="The scan name. This is used to label folders, scans and so on.", metavar="NAME")
        self.parser.add_option("-s", "--start", dest="start", default=settings.get('vna', 'minFreq'), help="The start frequency of the scan. You can use k,m and g for KHz, MHz and GHz.", metavar="START")
        self.parser.add_option("-e", "--stop", dest="stop", default=settings.get('vna', 'maxFreq'), help="The stop frequency of the scan. You can use k,m and g for KHz, MHz and GHz.", metavar="STOP")
        self.parser.add_option("-p", "--points", dest="points", type="int", help="Number of scan points. Can be specified instead of steps.", metavar="POINTS")
        self.parser.add_option("-t", "--step", dest="step", help="Scan steps. Can be specified instead of points. You can use k,m and g for KHz, MHz and GHz.", metavar="STEP")
        self.parser.add_option("-r", "--runs", dest="runs", type="int", default=1, help="Number of scan runs. If you want to average, you need more than one run.", metavar="RUNS")
        self.parser.add_option("-a", "--average", dest="average", action="store_true", help="Calculates an average out of multiple scan runs.", metavar="average")
        self.parser.add_option("-c", "--csv", dest="csv", action="store_true", help="Generate csv files for this scan.", metavar="CSV")
        self.parser.add_option("-u", "--truncate", dest="truncate", type="int", default=0, help="Truncate values before averaging. This helps with measurement errors. Truncates x times the min and max of the scans. So you need more runs than this factor*2", metavar="TRUNCATE")
        self.parser.add_option("-k", "--peaks", dest="peaks", type="int", help="Calculate peaks of the measurement. The cutoff factor specified is the return loss in db cutoff for peaks.", metavar="CUTOFF")
        self.parser.add_option("-l", "--plots", dest="plots", action="store_true", help="Generate plot files for this scan.", metavar="PEAKS")
        self.parser.add_option("-d", "--delay", dest="delay", type="int", help="Sets an eDelay for the whole scan.", metavar="DELAY")
        self.parser.add_option("-y", "--overwrite", dest="overwrite", action="store_true", help="Overwrite scans with the same name.", metavar="OVERWRITE")


    def verifyArgs(self, opt, args) -> None:
        if not opt.name:
            errorMsg = "You need to specify a scan name with -n"
            log.error(errorMsg)
            self.parser.error(errorMsg)

        if opt.start: opt.start = self.formatFrequency(opt.start)
        if opt.stop: opt.stop = self.formatFrequency(opt.stop)
        if opt.step: opt.step = self.formatFrequency(opt.step)

        if opt.start < int(settings.get('vna', 'minFreq')) or opt.start > int(settings.get('vna', 'maxFreq')):
            errorMsg = f"The start frequency needs to be between {float(settings.get('vna', 'minFreq'))/1e6} MHz and {float(settings.get('vna', 'maxFreq'))/1e6} MHz"
            log.error(errorMsg)
            self.parser.error(errorMsg)

        if opt.stop < int(settings.get('vna', 'minFreq')) or opt.stop > int(settings.get('vna', 'maxFreq')):
            errorMsg = f"The stop frequency needs to be between {float(settings.get('vna', 'minFreq'))/1e6} MHz and {float(settings.get('vna', 'maxFreq'))/1e6} MHz"
            log.error(errorMsg)
            self.parser.error(errorMsg)

        if opt.start >= opt.stop:
            errorMsg = f"The start frequency must be smaller than the stop frequency"
            log.error(errorMsg)
            self.parser.error(errorMsg)

        if opt.step and opt.points:
            errorMsg = "You need to specify eighter points with -p or steps with -t and not both"
            log.error(errorMsg)
            self.parser.error(errorMsg)

        if opt.step and not opt.points:
            opt.points = False

        if not opt.step and opt.points:
            opt.step = False

        if not opt.step and not opt.points:
            opt.points = 101
            opt.step = False

        if opt.step and opt.step < 1:
            errorMsg = f"The minimal step is 1Hz"
            log.error(errorMsg)
            self.parser.error(errorMsg)

        if opt.runs == 1 and opt.average:
            errorMsg = "Calculating averages only works with multiple runs"
            log.error(errorMsg)
            self.parser.error(errorMsg)

        if opt.truncate and not opt.average:
            opt.average = True

        if opt.peaks and opt.runs > 1:
            opt.average = True

        if opt.truncate and opt.runs <= opt.truncate * 2:
            errorMsg = f"You must have more runs than you truncate * 2. You specified {opt.runs} Runs and want to truncate {opt.truncate}"
            log.error(errorMsg)
            self.parser.error(errorMsg)


    def formatFrequency(self, freqencyString: str) -> int:
        outFrequencyHz = 0

        reFrequency = re.search("\d*\.?\d*", freqencyString)
        reUnit = re.search("[kKmMgG]", freqencyString)

        if reFrequency and reUnit:
            unit = reUnit.group().lower()
            frequency = float(reFrequency.group())
            if unit == "k": outFrequencyHz = frequency * 1e3
            if unit == "m": outFrequencyHz = frequency * 1e6
            if unit == "g": outFrequencyHz = frequency * 1e9
        elif reFrequency and not reUnit:
            outFrequencyHz = reFrequency.group()

        if float(outFrequencyHz) < 1: outFrequencyHz = 0

        return int(outFrequencyHz)


    def getOpts(self):
        return self.opt
