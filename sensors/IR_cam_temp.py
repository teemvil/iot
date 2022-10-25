import time
import busio
import board
import adafruit_amg88xx
import paho.mqtt.client as mqtt
import json
import math

import socket

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

IP="192.168.11.79"
PORT=1883

client = mqtt.Client()
client.connect(IP, PORT, 60)

payload = {
    "hostname": socket.gethostname(),
    "message": ""
}

payload["message"]= "IR sensor started on device"
client.publish(f"management", json.dumps(payload))

payload["message"]= "IR sensor transmitting data"
client.publish(f"management", json.dumps(payload))
while True:
    #client.publish("sensor/temperature", payload=amg.temperature)
    #client.publish("pixel/temperature", payload=json.dumps(amg.pixels))
    
    mean = 0
    for column in amg.pixels:
        mean = sum(column) / len(amg.pixels)
        
    client.publish("data/iotpi014/sensor/ir/pixels", payload=math.floor(mean))
    client.publish("data/iotpi014/sensor/ir/temperature", payload=math.floor(mean))
    
    if mean > 24:
        client.publish("alert", payload="Hot!")
    time.sleep(2)
