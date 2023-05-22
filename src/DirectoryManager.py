from src.Logger import log

import os
import shutil

class DirectoryManager:

    rootDirInitialized = False

    def __init__(self, scanName: str) -> None:
        self.scanName = scanName


    def initRootDir(self) -> None:
        log.info(f"Initiating Root Directory of scan: output/{self.scanName}")

        path = f"output/{self.scanName}"

        if os.path.exists(path):
            log.info(f"Directory {path} already exists.")
            inputKey = input(f"The scan '{self.scanName}' already exists. Overwrite? [y/n]: ")
            if inputKey == "y":
                log.info(f"Overwriting direcory {path}")
                shutil.rmtree(path)
            else:
                log.info(f"Overwriting direcory {path} canceled. Exiting.")
                exit()

        self.rootDirInitialized = True
        os.mkdir(path)


    def initDir(self, name: str) -> str:
        if not self.rootDirInitialized: self.initRootDir()

        path = f"output/{self.scanName}/{name}"
        if not os.path.exists(path):
            log.info(f"Initiating {name} Directory of scan: {path}")
            os.mkdir(path)

        return path
