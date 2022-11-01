from device.InitObject import InitObject
import json


class Sensor(InitObject):

    def __init__(self):
        super().__init__()
    
    def run(self):
        self.client.connect()

        self.client.publish('test', json.dumps({'message': 'from sensor'}))
        
