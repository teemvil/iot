import time
import board
import busio
import adafruit_vl53l0x
import paho.mqtt.client as mqtt
import json

import socket

i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
vl53.measurement_timing_budget = 33000

IP="192.168.11.79"
PORT=1883

client = mqtt.Client()
client.connect(IP, PORT, 60)

alert_status = False

with vl53.continuous_mode():
    #print(vl53.is_continuous_mode)
    #print(vl53.distance)
    #print("ToF sensor started on device: " + socket.gethostname())
    client.publish("management", payload = socket.gethostname() + ": ToF sensor started.")

    while True:
        
        if (vl53.range<800):
            #client.publish("management", payload = socket.gethostname() + ": ToF sensor recording a precense under 80cm.")
            client.publish("alert", payload = socket.gethostname() + ": Precense detected!")
            #print("Precense detected")
            alert_status = True
        else:
            alert_status = False

        while alert_status:

            if (vl53.data_ready):

                curTime = time.time()
                
                if (vl53.range<800):
                    #print ("Range: {0}mm".format(vl53.range))            
                    client.publish("data/iotpi016/sensor/tof", payload=vl53.range)
                    time.sleep(1.0)
                else:
                    #client.publish("management", payload = socket.gethostname() + ": ToF sensor recording stopped")
                    client.publish("alert", payload = socket.gethostname() +  ": No precense detected.")
                    #print("Precense left")
                    alert_status=False

