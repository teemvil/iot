import device_manager
import attestation
import paho.mqtt.client as mqtt
import json
import threading


def setup():
    mgr = device_manager
    att = attestation
    t1 = threading.Thread(target=mgr.run)
    t2 = threading.Thread(target=att.run)
    t1.start()
    t2.start()


def start():
    client = mqtt.Client()
    client.connect('127.0.0.1')

    client.publish("management", payload=json.dumps(
        {'operation': 'process-startup'}))

    client.publish("management", payload=json.dumps(
        {'operation': 'attest', 'type': 'process-startup'}))


if __name__ == '__main__':
    setup()
    start()
