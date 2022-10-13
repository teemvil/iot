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

while True:
    print("sensor/lux: " + str(tsl.lux))
    client.publish("data/iotpi015/sensor/lux", payload=tsl.lux)
    if float(tsl.lux) > 45:
         client.publish("alert/lux", payload="Alert, brightness is over 45")
    #client.publish("pixel/temperature", payload=json.dumps(amg.pixels))
    time.sleep(2)