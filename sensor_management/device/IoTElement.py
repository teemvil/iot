import paho.mqtt.client as mqtt
import json


class IoTElement:

    def __init__(self):
        self.client = mqtt.Client()
        self.config = self.__read_data()
        self.client_config = self.__read_config()
        self.ip = self.client_config["host"]
        self.port = self.client_config["port"]
        self.keepalive = self.client_config["keepalive"]
        self.client.connect(self.ip, self.port, self.keepalive)

    def __read_config(self):
        with open('/etc/iotDevice/config.json', 'r') as f:
            return json.loads(f.read())

    def __read_data(self):
        with open('/etc/iotDevice/device.json', 'r') as f:
            return json.loads(f.read())

    def run(self):
        print("IoTElement RUN")
