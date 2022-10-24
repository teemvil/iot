#!/bin/env python3
import paho.mqtt.client as mqtt
import socket
import json
import requests
import os

client = mqtt.Client()
client.connect("192.168.11.79", 1883, 60)

hostname = socket.gethostname()
url = f"http://192.168.11.79:8520/element/name/{hostname}"

response = requests.get(url).json()
id = response["itemid"]

payload = {
    "itemid": id,
    "hostname": hostname
    "operation": "startup"
}

client.publish(f"management", json.dumps(payload))

# Currently the path is just a test file
# If everything is ok start the device manager here:
os.system("python3 /home/metropolia/Innovationproject2022/controller/device_manager/test.py")
