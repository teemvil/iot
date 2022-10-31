from device.InitObject import InitObject
import json
import time


class Sensor(InitObject):

    def __init__(self):
        super().__init__()

    def start_up(self):
        self.connect()
        self.client.publish('management', json.dumps(self.config))

        self.client.subscribe('management/iotpi014')
        self.client.on_message = self.on_message
    
    def on_message(self, client, userdata, msg):
        client.publish('data', json.dumps({'testdata': 'testdata'}))
    