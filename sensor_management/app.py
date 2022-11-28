from device.sensors.RngSensor import RngSensor
import threading
import json


def start():
    x = RngSensor()
    x.measure_stuff()

if __name__ == '__main__':
    start()
