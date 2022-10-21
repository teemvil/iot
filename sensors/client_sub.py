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
lux_q = queue.LifoQueue()
tof_q = queue.LifoQueue()
temp_q = queue.LifoQueue()
pix_q = queue.LifoQueue()

def handleAlert(payload):
    print("alert detected: " + payload)

def handleManagement(payload):
    print("management message detected: " + payload)

dataCount = 0
def handleData(topic, payload):
    global dataCount
    global lux_q
    global tof_q
    global pix_q
    global temp_q

    if topic == "data/iotpi015/sensor/lux":
        lux_q.put(payload, "lux")

    if topic == "data/iotpi014/sensor/ir/temperature":
        temp_q.put(payload, "temp")
    
    if topic == "data/iotpi014/sensor/ir/pixels":
        pix_q.put(payload, "pix")    

    if topic == "data/iotpi016/sensor/tof":
        tof_q.put(payload, "tof")
    
    dataCount = dataCount +1

    if dataCount>50:
        lq=lux_q.get()
        tq=tof_q.get()
        #print("From lux queue: " + str(lq) + "; From tof queue: " + str(tq))
        getFromQueue()
        dataCount=0
    

def getFromQueue():
    print("From lux queue: " + str(lux_q.get()) + "; From tof queue: " + str(tof_q.get()))

def processMessage(payload, topic):
    print(topic+" "+str(payload))   

    if topic == "alert":
        handleAlert(payload)

    else:
        if topic == "management":
            handleManagement(payload)
        else:
            handleData(topic, payload)


def on_message(client, userdata, msg):
    
    x = threading.Thread(target=processMessage, args=(msg.payload, msg.topic))
    x.start()




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(IP, PORT, 60)

client.loop_forever()
