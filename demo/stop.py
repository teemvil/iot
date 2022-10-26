import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect('127.0.0.1')
client.publish('management', payload=json.dumps({'operation': 'kill-process'}))