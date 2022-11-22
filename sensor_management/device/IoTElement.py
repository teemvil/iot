import paho.mqtt.client as mqtt
import json


class IoTElement:

    def __init__(self):
        self.client = mqtt.Client()
        self.device_config = self.read_config_file(
            '/etc/iotDevice/device_config.json')
        self.client_config = self.read_config_file(
            '/etc/iotDevice/client_config.json')

        self.ip = self.client_config["host"]
        self.port = self.client_config["port"]
        self.keepalive = self.client_config["keepalive"]
        self.client.connect(self.ip, self.port, self.keepalive)

        self.message = {
            "event": "",
            "message": "",
            "messagetimestamp": "",
            "device": {
                "itemid": "",
                "hostname": self.device_config["hostname"],
                "address": "",
                "starttimestamp": "",
                "valid": False,
                "validtimestamp": ""
            },
            "sensor": {
                "name": "",
                "starttimestamp": "",
                "valid": False,
                "validtimestamp": ""

            }
        }

    def read_config_file(self, path):
        with open(path, 'r') as f:
            return json.loads(f.read())
