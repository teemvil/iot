import paho.mqtt.client as mqtt
import json 


class InitObject:

    def __init__(self):
        self.client = mqtt.Client()
        self.config = self.read_config()
        self.ip = '192.168.11.79'
        self.port = 1883

    def read_config(self):
        with open('device/config.json', 'r') as f:
            return json.loads(f.read())

    def connect(self):
        self.client.connect(self.ip, self.port, 60)