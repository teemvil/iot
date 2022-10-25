import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
import socket
import threading
import sys
import importlib
from pathlib import Path

data_folder = Path("/etc/iotDevice/")

sensor = importlib.load_module(sys.argv[1])

IP="192.168.11.79"
PORT=1883

json_object = {}

def open_json():
    # Määritettävä tiedostopolku ja nimi
    with open('sample.json', 'r') as openfile:    
        global json_object 
        json_object = json.load(openfile)    
        print(json_object)
        print(type(json_object))

    send_message()

def send_message ():
    global json_object
    json_object["operation"]= "Device manager started"
    print(json_object)
    client.publish(f"management", json.dumps(json_object))
    sensor_start()

def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe("management")
    open_json()

def sensor_start ():
    global json_object
    json_object["operation"]= "Device manager starting device"
    client.publish(f"management", json.dumps(json_object))
    #start sensors

def processMessage(payload, topic):
    print(topic+" "+str(payload))
    # toiminnallisuus kaikkiin päivityksiin, uudelleenkäynnistys tms.

def on_message(client, userdata, msg):    
    x = threading.Thread(target=processMessage, args=(msg.payload, msg.topic))
    x.start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(IP, PORT, 60)

client.loop_forever()