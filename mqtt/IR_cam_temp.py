import time
import busio
import board
import adafruit_amg88xx
import paho.mqtt.client as mqtt
import json

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

IP="192.168.11.79"
PORT=1883

client = mqtt.Client()
client.connect(IP, PORT, 60)

while True:
    client.publish("sensor/temperature", payload=amg.temperature)
    client.publish("pixel/temperature", payload=json.dumps(amg.pixels))
    time.sleep(2)
