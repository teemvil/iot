from sensor import Sensor
import time
import busio
import board
import adafruit_tsl2561
import paho.mqtt.client as mqtt
import json
import math

class LuxSensor(Sensor):
    i2c = busio.I2C(board.SCL, board.SDA)
    tsl = adafruit_tsl2561.TSL2561(i2c)

    
    client = mqtt.Client()
    
    def __init__(self):
        super().__init__()
        self.client.publish("management", payload=json.dumps({"name": "iotpi15", "message": "Lux sensor is on"}))
    
    
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
            time.sleep(2)
    
    def start_up():
        print("test")