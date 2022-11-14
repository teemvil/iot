from device.sensors.BasicSensor import BasicSensor
import time
import busio
import board
import adafruit_amg88xx
import paho.mqtt.client as mqtt
import json
import math

class IrSensor(BasicSensor):
    # Sensor specific variables
    i2c = busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c)


    def __init__(self, f, n) -> None:
       super().__init__(n)
       self.frequency = f

    def measure_stuff(self):       
         while True:
            mean = 0
            for column in self.amg.pixels:
                mean = sum(column) / len(self.amg.pixels)

            self.publish_data(math.floor(payload=math.floor(mean)))
            time.sleep(self.frequency)

