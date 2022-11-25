from device.sensors.BasicSensor import BasicSensor
import time
import busio
import board
import adafruit_amg88xx
import paho.mqtt.client as mqtt
import json
import math

class IR_cam(BasicSensor):
    # Sensor specific variables
    i2c = busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c)


    def __init__(self) -> None:
       super().__init__()

    def measure_stuff(self):       
         while True:
            mean = 0
            for column in self.amg.pixels:
                mean = sum(column) / len(self.amg.pixels)

            self.publish_data(round(mean, 2), self.data_topic_end)
            time.sleep(self.frequency)

