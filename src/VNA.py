from src.Logger import log

import serial
from serial.tools import list_ports

class VNA:

    port = False
    serial = False


    def __init__(self, VID: int, PID: int) -> None:
        self.port = self.findport(VID, PID)
        self.open()


    def findport(self, VID: int, PID: int) -> str:
        devicePort = False
        port_list = list_ports.comports()

        for port in port_list:
            if port.vid == VID and port.pid == PID:
                devicePort = port.device
                log.info(f"Successfully connected to: {devicePort}")

        if not devicePort:
            log.critical(f"Could not find a valid device with VID '{VID}' and PID '{PID}'")
            exit()

        return devicePort


    def open(self) -> None:
        if self.serial is False or None:
            self.serial = serial.Serial(self.port)


    def close(self) -> None:
        if self.serial:
            self.serial.close()
        self.serial = None


    def write(self, cmd: str) -> None:
        self.open()
        self.serial.write(cmd.encode())
        self.serial.readline() # discard empty line


    def read(self) -> str:
        result = ""
        line = ""

        while True:
            c = self.serial.read().decode("utf-8")
            if c == chr(13):
                next
            line += c
            if c == chr(10):
                result += line
                line = ""
                next
            if line.endswith("ch>"):
                break
        return result


    def setDelay(self, picoSec: int = 0) -> None:
        self.write(f"edelay {picoSec}\r")


    def resume(self) -> None:
        self.write("resume\r")
