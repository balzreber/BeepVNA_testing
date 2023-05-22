import logging
import logging.handlers

from src.Settings import settings

class Logger:

    logger = False

    def __init__(self):
        logLevel = self.getLogLevel(settings.get('logging', 'logLevel'))
        format = settings.get('logging', 'format')
        maxSizeMb = int(settings.get('logging', 'maxSizeMb'))
        keepLogs = int(settings.get('logging', 'keepLogs'))
        consoleLogLevel = self.getLogLevel(settings.get('logging', 'consoleLogLevel'))
        consoleFormat = settings.get('logging', 'consoleFormat')

        self.logger = self.createLogger('beepVna', logLevel)

        fileHandler = self.createFileHandler('logs/beepVna.log', maxSizeMb, keepLogs, logLevel, format)
        self.logger.addHandler(fileHandler)

        consoleHandler = self.createConsoleHandler(consoleLogLevel, consoleFormat)
        self.logger.addHandler(consoleHandler)


    def createLogger(self, name, logLevel):
        logger = logging.getLogger(name)
        logger.setLevel(logLevel)

        return logger


    def createFileHandler(self, path, maxSizeMb, backupCount, logLevel, format):
        maxBytes = maxSizeMb * 1e6

        fileHandler = logging.handlers.RotatingFileHandler(path, maxBytes = maxBytes, backupCount = backupCount)
        fileHandler.setLevel(logLevel)

        fileFormatter = logging.Formatter(format)
        fileHandler.setFormatter(fileFormatter)

        return fileHandler


    def createConsoleHandler(self, logLevel, format):
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logLevel)

        consoleFormatter = logging.Formatter(format)
        consoleHandler.setFormatter(consoleFormatter)

        return consoleHandler


    def activateScanLog(self, scanName):
        log.info("ScanLog started")

        path = f"output/{scanName}/{scanName}.log"

        self.scanHandler = logging.FileHandler(path, mode='w')
        self.scanHandler.setLevel(self.getLogLevel(settings.get('logging', 'scanLogLevel')))

        scanFormatter = logging.Formatter(settings.get('logging', 'scanFormat'))
        self.scanHandler.setFormatter(scanFormatter)

        self.logger.addHandler(self.scanHandler)


    def deactivateScanLog(self):
        log.info("ScanLog terminated")
        self.logger.removeHandler(self.scanHandler)


    def getLogLevel(self, name):
        if name == 'DEBUG': return logging.DEBUG
        elif name == 'INFO': return logging.INFO
        elif name == 'WARNING': return logging.WARNING
        elif name == 'ERROR': return logging.ERROR
        elif name == 'CRITICAL': return logging.CRITICAL
        else: raise Exception("Log Level must me 'DEBUG', 'INFO', 'WARNING', 'ERROR' or 'CRITICAL'")


    def getLog(self):
        return self.logger



logger = Logger()
log = logger.getLog()
