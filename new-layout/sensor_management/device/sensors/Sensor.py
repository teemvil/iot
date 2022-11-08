from device.InitObject import InitObject
from device.Manager import Manager
import json
import time
import math
import time
import threading


class Sensor(InitObject):
    def __init__(self):
        super().__init__()

    def start_up(self):
        self.connect()
        self.client.publish('management', json.dumps(self.config))

        self.client.subscribe('management/iotpi014')
        self.client.on_message = self.on_message

        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        pass
