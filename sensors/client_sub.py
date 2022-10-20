import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
import ast
import threading
#from colors import *
import argparse
import queue
from queue import Queue

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

q = queue.Queue()

def handleAlert(payload):
    print("alert detected: " + payload)

def handleManagement(payload):
    print("management message detected: " + payload)

dataCount = 0
def handleData(topic, payload, q):

    if topic == "data/iotpi015/sensor/lux":
        q.push(payload, "lux")

    if topic == "data/iotpi014/sensor/ir/temperature":
        q.push(payload, "temp")
    
    if topic == "data/iotpi014/sensor/ir/pixels":
        q.push(payload, "pix")    

    if topic == "data/iotpi016/sensor/tof":
        q.push(payload, "tof")
    
    dataCount = dataCount +1

    if dataCount>50:
        print(str(q.pull))
        dataCount=0
    

def getFromQueue():
    print(str(q.pull))

def processMessage(payload, topic, q):
    print(topic+" "+str(payload))   

    if topic == "alert":
        handleAlert(payload)

    else:
        if topic == "management":
            handleManagement(payload)
        else:
            handleData(topic, payload, q)


def on_message(client, userdata, msg):
    
    x = threading.Thread(target=processMessage, args=(msg.payload, msg.topic, q))
    x.start()




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(IP, PORT, 60)

client.loop_forever()
