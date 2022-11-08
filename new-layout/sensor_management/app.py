from multiprocessing.dummy import Manager

from device.Device import Device
from device.sensors.Sensor import Sensor
from device.sensors.RngSensor import RngSensor
from device.Manager import Manager
import threading
import json
import sys


def start():
    s = RngSensor()
    m = Manager(s)

    m.run()




if __name__ == '__main__':
    start()
