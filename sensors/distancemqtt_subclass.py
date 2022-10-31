import time
import board
import busio
import adafruit_vl53l0x
import paho.mqtt.client as mqtt
import json

import socket

from sensor import Sensor

class DistanceSensor(Sensor):
    i2c = busio.I2C(board.SCL, board.SDA)
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)
    vl53.measurement_timing_budget = 33000


    IP="192.168.11.79"
    PORT=1883

    client = mqtt.Client()
    client.connect(IP, PORT, 60)

    alert_status = False
    payload = {
    "hostname": socket.gethostname(),
    "message": ""
    }
    
    def __init__(self):
        super().__init__()


    def send_message():
        print("test")
        
        
    def measure_stuff(self):
        with self.vl53.continuous_mode():
            #print(vl53.is_continuous_mode)
            #print(vl53.distance)
            #print("ToF sensor started on device: " + socket.gethostname())
            self.client.publish("management", payload = socket.gethostname() + ": ToF sensor started.")

            while True:
                
                if (self.vl53.range<800):
                    #client.publish("management", payload = socket.gethostname() + ": ToF sensor recording a precense under 80cm.")
                    self.client.publish("alert", payload = socket.gethostname() + ": Precense detected!")
                    #print("Precense detected")
                    alert_status = True
                else:
                    alert_status = False

                while alert_status:

                    if (self.vl53.data_ready):

                        curTime = time.time()
                        
                        if (self.vl53.range<800):
                            #print ("Range: {0}mm".format(vl53.range))            
                            self.client.publish("data/iotpi016/sensor/tof", payload=self.vl53.range)
                            time.sleep(1.0)
                        else:
                            #client.publish("management", payload = socket.gethostname() + ": ToF sensor recording stopped")
                            self.client.publish("alert", payload = socket.gethostname() +  ": No precense detected.")
                            #print("Precense left")
                            alert_status=False
    
    def start_up():
        print("test")