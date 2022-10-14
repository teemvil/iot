import time
import busio
import board
import adafruit_tsl2561
import paho.mqtt.client as mqtt
import json

i2c = busio.I2C(board.SCL, board.SDA)
tsl = adafruit_ts12561.TSL2561(i2c)

IP="192.168.11.79"
PORT=1883

client = mqtt.Client()
client.connect(IP, PORT, 60)
status_old = bool(float(tsl.lux) > 46)
change = True

if status_old:
     client.publish("alert/iotp015/lux", payload="Status: Light")
     print("Status: Light")
else:
     client.publish("alert/iotp015/lux", payload="Status: Dark")
     print("Satus: Dark")

while True:
     print("sensor/lux: " + str(tsl.lux))
     client.publish("data/iotpi015/sensor/lux", payload=tsl.lux)

     status = bool(float(tsl.lux) > 46)
     if status != status_old:
          change = True
     else:
          change = False

     if change:
          if status:
               client.publish("alert/iotp015/lux", payload="Status: Light")
               print("Status: Light")
          else:
               client.publish("alert/iotp015/lux", payload="Status: Dark")
               print("Satus: Dark")

     status_old = status
     time.sleep(2)
