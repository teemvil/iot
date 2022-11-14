from device.sensors.RngSensor import RngSensor
import threading
import json


def start():
    x = RngSensor('rngsensor')
    x.run()

if __name__ == '__main__':
    start()
