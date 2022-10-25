import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
import ast
import threading
import argparse
import queue
from queue import Queue
import csv
from datetime import datetime
import math
import requests

IP="192.168.11.79"
PORT=1883

# Starts listening to changes in the topic given to the client.subscribe() function.
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


# Create new file 
def createNewFile(name):
    file=open(name, "w")
    writer=csv.writer(file)
    # Create header row
    writer.writerow(["lux", "tof", "temp", "pix", "time"])
    file.close()

# Always create new file when program starts
t = datetime.now()
filename="test-"+str(t.strftime('%m-%d-%Y_%H-%M-%S'))+".csv"
createNewFile(filename)


def takePicture():
    if lux_status:
        if IR_status:
            if tof_status:
                url = "http://192.168.11.125/api/images"
                response = requests.get(url)
                print(response)
                print("Taking a picture!!!")
                client.publish("alert", payload=("PICTIRE TAKESN!!!"))


# Handles incoming alert messages
def handleAlert(payload):
    print("alert detected: " + payload)

# Handles incoming management messages
def handleManagement(payload):
    print("management message detected: " + payload)

# Datacounter for data handling
dataCount = 0
# Default statuses is false
lux_status = False
tof_status = False
IR_status = False
# Handles incoming data payloads
def handleData(topic, payload):
    global dataCount
    global lux_q
    global tof_q
    global pix_q
    global temp_q
    global lux_status
    global tof_status
    global IR_status

    # Handle data and put the data in appropriate queue
    if topic == "data/iotpi015/sensor/lux":
        lux_q.put(payload, "lux")

        change = True
        
        status = bool(float(payload) > 46)
        if status != lux_status:
            change = True
        else:
            change = False

        if change:
            if status:
                client.publish("alert", payload=json.dumps({"name": "iotp015", "message": "Status: Light"}))
                print("Status: Light")
            else:
                client.publish("alert", payload=json.dumps({"name": "iotp015", "message": "Status: Dark"}))
                print("Satus: Dark")

        lux_status = status

    if topic == "data/iotpi014/sensor/ir/temperature":
        temp_q.put(payload, "temp")
    
    if topic == "data/iotpi014/sensor/ir/pixels":
        pix_q.put(payload, "pix")    

        change = True
        
        status = bool(float(payload) > 24)
        if status != IR_status:
            change = True
        else:
            change = False

        if change:
            if status:
                client.publish("alert", payload=json.dumps({"name": "iotp014", "message": "Status: HOT"}))
                print("Status: HOT")
            else:
                client.publish("alert", payload=json.dumps({"name": "iotp014", "message": "Status: COLD"}))
                print("Satus: COLD")
        
        IR_status=status

    if topic == "data/iotpi016/sensor/tof":
        tof_q.put(payload, "tof")

        change = True
        
        status = bool(float(payload) > 800)
        if status != tof_status:
            change = True
        else:
            change = False

        if change:
            if status:
                client.publish("alert", payload=json.dumps({"name": "iotp016", "message": "Status: presence detected"}))
                print("Status: presence")
            else:
                client.publish("alert", payload=json.dumps({"name": "iotp016", "message": "Status: presence not detected"}))
                print("Satus: NO presence")
        
        tof_status=status
    
    dataCount = dataCount +1

    # Calls the data save function for every *20* data points gathered
    if dataCount>20:
        dataCount=0
        getFromQueues()
    

# Save counter for queue process
saveCount=0
# Saves data from the queues to a csv file
def getFromQueues():
    if lux_q.empty():
        lq = 0
    else:
        lq=lux_q.get()
    
    if tof_q.empty():
        tq = 0
    else:
        tq=tof_q.get()

    if temp_q.empty():
        teq = 0
    else:
        teq=temp_q.get()

    if pix_q.empty():
        pixq = 0
    else:
        pixq=temp_q.get()

    # Because get() pulls the value out of the queue, they have to be put back in,
    # just in case there are no new values before the next pull. 
    # If not done, the queue would go backwards in time.
    lux_q.put(lq)
    tof_q.put(tq)
    temp_q.put(teq)
    pix_q.put(pixq)

    print("From lux queue: " + str(lq) + "; From tof queue: " + str(tq) + "; from temp queue: " + str(teq) + "; from pix queue: " + str(pixq))
    
    # Write the data as a new row to file
    global filename
    global saveCount
    try:
        data =[int(lq), int(tq), int(teq), int(pixq), str(datetime.now())]
        file = open(filename, "a")
        writer = csv.writer(file)
        writer.writerow(data)
        file.close()
        saveCount = saveCount+1
    except:
        print("could not save file")
        # Could send an mqtt msg?
        
    # Creates a new file if *something*
    # Now it's just a counter but could be taking a pic or whatever...
    if saveCount > 100:
        t = datetime.now()
        filename="test-"+str(t.strftime('%m-%d-%Y_%H-%M-%S'))+".csv"
        createNewFile(filename)

    

# Sends message for appropriate sub-routines for handling
def processMessage(payload, topic):
    print(topic+" "+str(payload))   

    if topic == "alert":
        handleAlert(payload)

    else:
        if topic == "management":
            handleManagement(payload)
        else:
            handleData(topic, payload)


# Starts a processing thread everytime a message is received
def on_message(client, userdata, msg):
    x = threading.Thread(target=processMessage, args=(msg.payload, msg.topic))
    x.start()




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(IP, PORT, 60)

client.loop_forever()

# Default statuses: dark, no presence and cold
client.publish("alert", payload=json.dumps({"name": "iotp015", "message": "Status: Dark"}))
client.publish("alert", payload=json.dumps({"name": "iotp016", "message": "Status: presence not detected"}))
client.publish("alert", payload=json.dumps({"name": "iotp014", "message": "Status: COLD"}))
