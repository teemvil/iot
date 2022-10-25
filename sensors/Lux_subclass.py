from device import Device
import time
import busio
import board
import adafruit_tsl2561
import paho.mqtt.client as mqtt
import json
import math

class LuxSensor(Device):
    i2c = busio.I2C(board.SCL, board.SDA)
    tsl = adafruit_tsl2561.TSL2561(i2c)
    IP="192.168.11.79"
    PORT=1883
    
    client = mqtt.Client()
    client.connect(IP, PORT, 60)
    status_old = False
    change = True
    
    def __init__(self):
        super().__init__()
        self.status_old = bool(float(self.tsl.lux) > 46)
        self.client.publish("management", payload=json.dumps({"name": "iotpi15", "message": "Lux sensor is on"}))
        if self.status_old:
            self.client.publish("alert", payload=json.dumps({"name": "iotpi15", "message": "Status: Light"}))
            print("Status: Light")
        else:
            self.client.publish("alert", payload=json.dumps({"name": "iotpi15", "message": "Status: Dark"}))
            print("Satus: Dark")
    
    
    def send_message():
        print("test")
        
        
    def measure_stuff(self):
        print("measuring stuff")
        while True:
            print("sensor/lux: " + str(math.floor(self.tsl.lux)))

            dataload={
                "sensor": "lux",
                "data": math.floor(self.tsl.lux)
            }
            self.client.publish("data/iotpi015/sensor/lux", payload=math.floor(self.tsl.lux))

            status = bool(float(self.tsl.lux) > 46)
            if status != self.status_old:
                change = True
            else:
                change = False

            if change:
                if status:
                    self.client.publish("alert", payload=json.dumps({"name": "iotp015", "message": "Status: Light"}))
                    print("Status: Light")
                else:
                    self.client.publish("alert", payload=json.dumps({"name": "iotp015", "message": "Status: Dark"}))
                    print("Satus: Dark")

            status_old = status
            time.sleep(2)
    
    def start_up():
        print("test")