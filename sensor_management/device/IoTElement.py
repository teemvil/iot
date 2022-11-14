import paho.mqtt.client as mqtt
import json
import os


class IoTElement:

    def __init__(self):
        self.client = mqtt.Client()
        self.config = self.read_config()
        self.ip = self.config["client"]["host"]
        self.port = self.config["client"]["port"]
        self.client.connect(self.ip, self.port, 60)

    def read_config(self):
        here = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(here, 'config.json')

        with open(file_name, 'r') as f:
            return json.load(f)

    def run(self):
        print("IoTElement RUN")
