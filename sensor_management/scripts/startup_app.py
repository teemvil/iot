import paho.mqtt.client as mqtt
import socket
import json


def start():
    client = mqtt.Client()
    client.connect('192.168.11.79')

    payload = {
        "itemid": "",
        "hostname": "",
        "ip": "",
        "message": "",
        "event": "",
        "device": {
            "valid": False,
            "timestamp": ""
        },
        "sensor": {
            "name": "",
            "timestamp": ""
        },
        "timestamp": "",
        "client": {
            "host": "192.168.11.79",
            "port": 1883,
            "keepalive": 60
        }
    }

    client.publish('management', payload=json.dumps(payload))


if __name__ == '__main__':
    start()
