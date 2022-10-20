#!/bin/env python3
import paho.mqtt.client as mqtt
import socket
import json
import requests

client = mqtt.Client()
client.connect("192.168.11.79", 1883, 60)

hostname = socket.gethostname()
url = f"http://192.168.11.79:8520/element/name/{hostname}"

response = requests.get(url).json()
id = response["itemid"]

payload = {
    "itemid": id,
    "hostname": hostname
}

client.publish(f"management", json.dumps(payload))
