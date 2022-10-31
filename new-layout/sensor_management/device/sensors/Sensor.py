from device.InitObject import InitObject
import json
import time


class Sensor(InitObject):

    def __init__(self):
        super().__init__()

    def start_up(self):
        self.connect()
        while True:
            self.client.publish('management', json.dumps(self.config))
            time.sleep(2)
