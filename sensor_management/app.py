from device.sensors.TofSensor import ToFSensor
import threading
import json


def start():
    s = ToFSensor(1, "tof")
    s.measure_stuff()


if __name__ == '__main__':
    start()
