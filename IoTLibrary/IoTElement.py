import paho.mqtt.client as mqtt
import json


class IoTElement:

    def __init__(self):
        self.client = mqtt.Client()
        self.device_config = self.read_config_file(
            '/etc/iotDevice/device_config.json')
        self.client_config = self.read_config_file(
            '/etc/iotDevice/client_config.json')

        self.connect_to_mqtt_client()

        # This is just a a structure for the payload sent from different
        # parts of the program.
        self.message = {
            "event": "",
            "message": "",
            "messagetimestamp": "",
            "device": {
                "itemid": self.device_config["itemid"],
                "hostname": self.device_config["hostname"],
                "address": self.device_config["address"],
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

    def connect_to_mqtt_client(self):
        try:
            self.client.connect(
                self.client_config["host"],
                self.client_config["port"],
                self.client_config["keepalive"]
            )
        except ValueError:
            print("Cannot connect to MQTT broker.")

    def read_config_file(self, path):
        try:
            with open(path, 'r') as f:
                return json.loads(f.read())
        except IOError:
            print("file opening not succesfull")
