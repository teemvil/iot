import paho.mqtt.client as mqtt
import socket
import json
import socket


def start():
    client = mqtt.Client()
    client.connect('192.168.0.24', 1883, 60)

    payload = {
        "itemid": "",
        "hostname": "iotpi014",
        "ip": "",
        "message": "start iot device",
        "event": "start device",
        "device": {
            "valid": "false",
            "timestamp": ""
        },
        "sensor": {
            "name": "",
            "timestamp": ""
        },
        "timestamp": "",
        "host": "192.168.0.24",
        "port": 1883,
        "keepalive": 60
    }

    client.publish('management', payload=json.dumps(payload))


if __name__ == '__main__':
    start()
