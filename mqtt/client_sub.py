import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
import ast
import threading
from colors import *
import argparse

IP="192.168.11.79"
PORT=1883

# This is just a testing function. It listens to changes in the topic given to the
# client.subscribe() function.
def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))

    client.subscribe("alert")
    client.subscribe("management")
    client.subscribe("data/iotpi015/sensor/lux")
    client.subscribe("data/iotpi014/sensor/ir/temperature")
    client.subscribe("data/iotpi014/sensor/ir/pixels")
    client.subscribe("data/iotpi016/sensor/tof")

ap = argparse.ArgumentParser(description='Displays the log file in real-time')
args = ap.parse_args()

def processMessage(payload, topic):
    print(topic+" "+str(payload))

def on_message(client, userdata, msg):
    if args.nottheaded==False:
        x = threading.Thread(target=processMessage, args=(msg.payload, msg.topic,))
        x.start()
    else:
        processMessage(msg.payload, msg.topic)
    


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(IP, PORT, 60)

client.loop_forever()
