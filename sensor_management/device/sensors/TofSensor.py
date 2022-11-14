from device.sensors.BasicSensor import BasicSensor
import time
import board
import busio
import adafruit_vl53l0x
import json


class ToFSensor(BasicSensor):
    # Sensor specific variables
    i2c = busio.I2C(board.SCL, board.SDA)
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)
    vl53.measurement_timing_budget = 33000

    def __init__(self, f, n) -> None:
        super().__init__(n)
        self.frequency = f

    def measure_stuff(self):       
        with self.vl53.continuous_mode():
            while True:
                if (self.vl53.data_ready):
                    time.sleep(self.frequency)
                    if (self.vl53.range < 1000):
                        self.publish_data(self.vl53.range)
    

