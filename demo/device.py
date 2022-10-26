import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client()
client.connect('127.0.0.1')

still_running = True

def validate():
    client.publish('management', payload=json.dumps(
        {'operation': 'attest', 'type': 'sensor-startup'}))

def stop():
    global still_running
    still_running = False

def measure_stuff():
    # Sensor specific implementation.
    while still_running:
        client.publish('data', payload=json.dumps({'data': '69.420'}))
        time.sleep(2)
