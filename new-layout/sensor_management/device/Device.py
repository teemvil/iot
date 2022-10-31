from device.InitObject import InitObject
import json
import time


class Device(InitObject):
    def __init__(self):
        super().__init__()

    def startup_message(self):
        self.connect()
        while True:
            self.client.publish('test', json.dumps({'message': 'startup'}))
            time.sleep(2)