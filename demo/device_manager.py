import device
import paho.mqtt.client as mqtt
import json
import threading

client = mqtt.Client()
client.connect('127.0.0.1')
sensor = device


def on_message(_client, userdata, msg):
    # Listen to management topic.
    x = json.loads(msg.payload)

    # This is just horrible xD
    if x['operation'] == 'verify' and x['type'] != 'sensor-startup':
        sensor.validate()
    elif x['operation'] == 'verify' and x['type'] == 'sensor-startup' and x['result'] == 'success':
        t = threading.Thread(target=sensor.measure_stuff)
        t.start()
    elif x['operation'] == 'kill-process':
        sensor.stop()


def send_alert():
    client.publish('alert', json.dumps({'message': 'verify not successful'}))


def stop_sensor():
    pass


def reboot():
    pass


def run():
    client.subscribe('management')
    client.on_message = on_message

    client.loop_forever()
