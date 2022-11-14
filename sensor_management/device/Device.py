from IoTElement import IoTElement
import json
import time

# Is this thing here needed?
# Change inheritance.
class Device(IoTElement):
    def __init__(self):
        super().__init__()

    def startup_message(self):
        self.connect()
        while True:
            self.client.publish('test', json.dumps({'message': 'startup'}))
            time.sleep(2)