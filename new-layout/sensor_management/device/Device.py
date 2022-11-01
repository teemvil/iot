from device.InitObject import InitObject
import json
import time


class Device(InitObject):
    def __init__(self, sensor):
        super().__init__()
        sensor = sensor

    def startup_message(self):
        self.connect()
        while True:
            self.client.publish('test', json.dumps({'message': 'startup'}))
            time.sleep(2)