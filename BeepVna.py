from src.VNA import VNA
from src.Scanner import Scanner
from src.DataSetProcessor import DataSetProcessor
from src.DirectoryManager import DirectoryManager
from src.Logger import log
from src.Logger import logger
from src.Settings import settings
from src.CLI import CLI
from src.Plotting import PlotTypes

import atexit
from datetime import datetime

version =  "0.1.0"

log.info("-- BeepVna started --")
log.info(f"BeepVna version {version}")

cli = CLI()
opt = cli.getOpts()

VID = int(settings.get('vna', 'VID'), 16)
PID = int(settings.get('vna', 'PID'), 16)
vna = VNA(VID, PID)

dirManager = DirectoryManager(opt.name)
processor = DataSetProcessor(opt.name, dirManager)

dirManager.initRootDir()
logger.activateScanLog(opt.name)


@atexit.register
def terminate():
    vna.resume()
    log.info(f"Time elapsed: {totalTime} (Scan: {scanTime} / PostProcessing {processingTime})")
    logger.deactivateScanLog()
    log.info("-- BeepVna terminated --")

if opt.delay:
    vna.setDelay(opt.delay)

startTime = datetime.now()

scanner = Scanner(vna, opt.name)

data = scanner.scan(opt.name, opt.start, opt.stop, points=opt.points, step=opt.step, runs=opt.runs)

scanStartTime = datetime.now()

processor.toNetwork(data, save = True)
if opt.csv: processor.toCsv(data, save = True)
if opt.plots: processor.toPlot(data, PlotTypes.LOGMAG, show = False, save = True)

if opt.average:
    average = processor.average(data, opt.truncate)

    processor.toNetwork(average, save = True)
    if opt.csv: processor.toCsv(average, save = True)
    if opt.plots: processor.toPlot(average, PlotTypes.LOGMAG, show = False, save = True)


if opt.peaks:
    if opt.average: peaks = processor.peaks(average, opt.peaks)
    else: peaks = processor.peaks(data, opt.peaks)

    processor.toNetwork(peaks, save = True)
    if opt.csv: processor.toCsv(peaks, save = True)
    if opt.plots:
        processor.toPlot(peaks, save = True)
        if opt.average: processor.toOverviewPlot(peaks, average.getDataSeries(), opt.peaks, PlotTypes.LOGMAG, show = False, save = True)
        else: processor.toPlot(peaks, data.getDataSeries(), opt.peaks, PlotTypes.LOGMAG, show = False, save = True)

scanTime = scanStartTime - startTime
processingTime = datetime.now() - scanStartTime
totalTime = datetime.now() - startTime
