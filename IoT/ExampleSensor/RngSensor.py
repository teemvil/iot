from IoTLibrary.BasicSensor import BasicSensor
import random
import time


class RngSensor(BasicSensor):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        while True:
            r = random.randint(1, 10)
            self.client.publish('alert', r)
            time.sleep(4)
