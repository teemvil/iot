from device.sensors.BasicSensor import BasicSensor
import json
import random
import time

class RngSensor(BasicSensor):
    def __init__(self, n):
        super().__init__(n)

    def run(self):
        while True:
            r = random.randint(1, 10)
            self.client.publish('alert', r)
            time.sleep(4)
