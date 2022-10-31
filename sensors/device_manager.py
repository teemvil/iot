import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
import socket
import threading
import sys
import importlib
import os
from pathlib import Path
from datetime import datetime

# Otetaan käyttöön, kun kutsu startup_app.sh on määritetty tai device abstarktiosta
# sensor = importlib.load_module(sys.argv[1])

IP="192.168.11.79"
PORT=1883

def start_devmngr(json_update):
    json_object = json_update
    json_object["message"]="Device manager started"
    json_object["event"]="dvmngr_start"
    json_object["timestamp"]= get_time_stamp()
    #print(json_object)
    client.publish(f"management", json.dumps(json_object))
    attest_validate(json_object)

def attest_validate(json_update):
    json_object=json_update
    json_object["event"] = "validation ok"
    json_object["message"] ="Device validation in process"
    json_object["device"]["valid"] = True
    client.publish(f"management/verify", json.dumps(json_object))

def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe("management")

def sensor_start (json_update):
    json_object=json_update
    json_object["message"]= "Device manager starting device"
    json_object["event"]= "sensorstart"
    json_object["timestamp"]= get_time_stamp()
    print("Sensor start")
    os.system("python3 /etc/sensors/*.py")

    client.publish(f"management", json.dumps(json_object))

def processMessage(payload, topic):
    print(topic+" "+str(payload))
    # Funcitonality for restart and reboot comes here

def on_message(client, userdata, msg):
    decoded_message=str(msg.payload.decode("utf-8"))
    json_object=json.loads(decoded_message)

    # startup.sh antaa event tietona startup
    if (msg.topic == "management" and json_object["hostname"]==socket.gethostname()):

        if (msg.topic == "management" and json_object["event"] == "startup"):
            start_devmngr(json_object)

        if (msg.topic == "management" and json_object["event"] == "validation ok" and json_object["device"]["valid"] == True):
            x = threading.Thread(target=processMessage, args=(msg.payload, msg.topic))
            x.start()
            sensor_start(json_object)
        else:
            json_object["message"]= "Device validation error"
            json_object["event"]= "dev_val_error"
            json_object["timestamp"]= get_time_stamp()
            #client.publish(f"management", json.dumps(json_object))
    """        
    if (msg.topic == "management" and json_object["hostname"]!=socket.gethostname())
        json_object["message"]="Device host names does not match"
        json_object["event"]="dev_name_error"
        json_object["timestamp"]=get_time_stamp()
        client.publish(f"alert", "Device host names does not match")
        client.publish(f"management", json.dumps(json_object))
    """

def get_time_stamp():
    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
    return date_time

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(IP, PORT, 60)

client.loop_forever()