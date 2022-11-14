import paho.mqtt.client as mqtt
import json


class IoTElement:

    def __init__(self):
        self.client = mqtt.Client()
        self.config = self.__read_config()
        self.ip = self.config["client"]["host"]
        self.port = self.config["client"]["port"]
        self.client.connect(self.ip, self.port, 60)

    def __read_config(self):
        with open('/etc/iotDevice/data_packet.json', 'r') as f:
            return json.loads(f.read())

    def run(self):
        print("IoTElement RUN")
