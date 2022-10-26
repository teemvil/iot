import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect('127.0.0.1')


def on_message(client, userdata, msg):
    x = json.loads(msg.payload)

    if x['operation'] == 'attest':
        verify(x)


def run():
    client.subscribe('management')
    client.on_message = on_message

    client.loop_forever()


def verify(x):
    client.publish('management', payload=json.dumps(
        {'operation': 'verify', 'type': x['type'], 'result': 'success'}))
    # pass
