from device.InitObject import InitObject
import paho.mqtt.client as mqtt
import json


class Manager(InitObject):
    def __init__(self):
        super().__init__()

    def on_message(self, client, userdata, msg):
        x = json.loads(msg.payload)

        if x.get('message') == 'startup':
            client.publish('test', json.dumps({'message': 'from manager'}))

    def listen(self):
        self.connect()

        self.client.subscribe('test')
        self.client.on_message = self.on_message
        self.client.loop_forever()
