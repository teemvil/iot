from sensor import Sensor
import time
import busio
import board
import adafruit_amg88xx
import paho.mqtt.client as mqtt
import json
import math
import socket

class IRSensor(Sensor):
    i2c = busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c)

    IP="192.168.11.79"
    PORT=1883

    client = mqtt.Client()
    client.connect(IP, PORT, 60)
    client.publish("management", payload="Iotpi014 IR sensor started")
    payload = {
    "hostname": socket.gethostname(),
    "message": ""
    }
    
    def __init__(self):
        super().__init__()
        self.payload["message"]= "IR sensor started on device"
        self.client.publish(f"management", json.dumps(self.payload))

        self.payload["message"]= "IR sensor transmitting data"
        self.client.publish(f"management", json.dumps(self.payload))

    
    
    def send_message():
        print("test")
        
        
    def measure_stuff(self):
        while True:
            #client.publish("sensor/temperature", payload=amg.temperature)
            #client.publish("pixel/temperature", payload=json.dumps(amg.pixels))
            mean = 0
            for column in self.amg.pixels:
                mean = sum(column) / len(self.amg.pixels)
                
            self.client.publish("data/iotpi014/sensor/ir/pixels", payload=math.floor(mean))
            self.client.publish("data/iotpi014/sensor/ir/temperature", payload=math.floor(mean))
            
            if mean > 24:
                self.client.publish("alert", payload="Hot!")
            time.sleep(2)
    
    def start_up():
        print("test")