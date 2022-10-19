import time
import busio
import board
import adafruit_tsl2561
import paho.mqtt.client as mqtt
import json
import math

i2c = busio.I2C(board.SCL, board.SDA)
tsl = adafruit_ts12561.TSL2561(i2c)

IP="192.168.11.79"
PORT=1883

client = mqtt.Client()
client.connect(IP, PORT, 60)
status_old = bool(float(tsl.lux) > 46)
change = True

client.publish("management", payload="iotpi015: lux sensor on")

if status_old:
     client.publish("alert", payload="iotpi15: Status: Light")
     print("Status: Light")
else:
     client.publish("alert", payload="iotpi015: Status: Dark")
     print("Satus: Dark")

while True:
     print("sensor/lux: " + str(math.floor(tsl.lux)))
     client.publish("data/iotpi015/sensor/lux", payload=math.floor(tsl.lux))

     status = bool(float(tsl.lux) > 46)
     if status != status_old:
          change = True
     else:
          change = False

     if change:
          if status:
               client.publish("alert", payload="iotp015: Status: Light")
               print("Status: Light")
          else:
               client.publish("alert", payload="iotp015: Status: Dark")
               print("Satus: Dark")

     status_old = status
     time.sleep(2)
