import time
import busio
import board
import adafruit_tsl2561
import paho.mqtt.client as mqtt
import math

class LuxSensor(BasicSensor):
     # Sensor specific variables
     i2c = busio.I2C(board.SCL, board.SDA)
     tsl = adafruit_ts12561.TSL2561(i2c)


     def __init__(self, f, n) -> None:
        super().__init__(n)
        self.frequency = f

     def measure_stuff(self):       
          while True:
              self.publish_data(math.floor(self.tsl.lux))
              time.sleep(self.frequency)
