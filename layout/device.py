import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect('127.0.0.1')


def validate():
    client.publish('management', payload=json.dumps(
        {'operation': 'attest', 'type': 'sensor-startup'}))


def measure_stuff():
    # Sensor specific implementation.
    client.publish('data', payload=json.dumps({'data': '69.420'}))
