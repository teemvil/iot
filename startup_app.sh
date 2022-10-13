#!/bin/python3
import paho.mqtt.client as mqtt
import socket
import json

client = mqtt.Client()
client.connect("192.168.11.79", 1883, 60)

payload = {
    "ID": "12345",
    "hostname": socket.gethostname(),
    "more_stuff": "hey you!"
}

client.publish("test/attestation", json.dumps(payload))