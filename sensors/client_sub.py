import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
import ast
import threading
#from colors import *
import argparse
import queue
from queue import Queue
import csv

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

# Create separate ques for each sensors' data
lux_q = queue.LifoQueue()
tof_q = queue.LifoQueue()
temp_q = queue.LifoQueue()
pix_q = queue.LifoQueue()

# Create new file on start of program
file=open("test.csv", "w")
writer=csv.writer(file)
# Create header row
writer.writerow(["lux", "tof", "temp", "pix"])
file.close()

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

    # Put the data in appropriate queue
    if topic == "data/iotpi015/sensor/lux":
        lux_q.put(payload, "lux")

    if topic == "data/iotpi014/sensor/ir/temperature":
        temp_q.put(payload, "temp")
    
    if topic == "data/iotpi014/sensor/ir/pixels":
        pix_q.put(payload, "pix")    

    if topic == "data/iotpi016/sensor/tof":
        tof_q.put(payload, "tof")
    
    dataCount = dataCount +1

    if dataCount>20:
        dataCount=0
        getFromQueues()
    

# Saves data from the queues to a csv file
def getFromQueues():
    if lux_q.empty() == True:
        lq = 0
    else:
        lq=lux_q.get()
    
    if tof_q.empty() == True:
        tq = 0
    else:
        tq=tof_q.get()

    if temp_q.empty() == True:
        teq = 0
    else:
        teq=temp_q.get()

    if pix_q.empty() == True:
        pixq = 0
    else:
        pixq=temp_q.get()

    print("From lux queue: " + str(lq) + "; From tof queue: " + str(tq) + "; from temp queue: " + str(teq) + "; from pix queue: " + str(pixq))
    
    # Write the data as a new row to file
    data =[int(lq), int(tq), int(teq), int(pixq)]
    file = open("test.csv", "a")
    writer = csv.writer(file)
    writer.writerow(data)
    file.close()


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
    # Starts a processing thread
    x = threading.Thread(target=processMessage, args=(msg.payload, msg.topic))
    x.start()




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(IP, PORT, 60)

client.loop_forever()
