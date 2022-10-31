from sensor import Sensor
import time
import board
import busio
import adafruit_vl53l0x
import paho.mqtt.client as mqtt
import json
import socket
import threading
from datetime import datetime

class ToFSensor(Sensor):

    i2c = busio.I2C(board.SCL, board.SDA)
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)
    vl53.measurement_timing_budget = 33000

    client = mqtt.Client()

    def __init__(self):
        super().__init__()
        payload = self.config
        IP = self.config["client"]["host"]
        PORT = self.config["client"]["port"]
        print (IP)
        print (PORT)
        print(payload)
        self.connect()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def start_up(self, json_load):
        payload = json_load
        with self.vl53.continuous_mode():
            #Viestin lähetys aggregaatio/UI, sensori päällä
            #print("start_ToF") #Tarkistus
            #print(vl53.is_continuous_mode) #Varmenne, että sensori päällä
            #print(vl53.distance) #Tarkistus
            payload["message"]= "ToF sensor started on device"
            payload["event"]="sensoronline"
            payload["sensor"]["timestamp"]=self.get_time_stamp()
            payload["sensor"]["name"]="Time of Flight"
            self.send_message(payload)
            self.measure_stuff(payload)

    def measure_stuff(self, json_object):
        payload=json_object
        #Viestin lähetys aggregaatio/UI, sensori kerää dataa
        #print("run_ToF") #Tarkisuts
        #print(vl53.is_continuous_mode) #Tarkistus
        payload["message"]= "ToF sensor running on device"
        payload["event"]="sensorrunning"
        self.send_message(payload)  
        try:
            payload["message"]="ToF sensor trasmitting data"
            payload["event"]="sensortrasmitting"
            self.send_message(payload) 
            while True:
                if (self.vl53.data_ready):
                    time.sleep(1.0)
                    #Mqtt dataa välikäteen kokoaika
                    if (self.vl53.range<1000):
                        self.client.publish("data/iotpi016/sensor/tof", payload=self.vl53.range)
                        print(self.vl53.range)
        except:
            #Viestin lähetys aggregaatio/UI, sensori lopetti toiminnan
            payload["message"]="ToF sensor stopped on device"
            payload["event"]="tof_error"
            self.send_message(payload)            
            self.vl53.stop_continuous()

    def send_message(self, json_object):
        payload=json_object
        self.client.publish(f"management", json.dumps(payload))

    def get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time

    def on_connect(self, client, userdata, flags, rc):
        print("connected with result code " + str(rc))
        self.client.subscribe("management")

    def on_message(self, client, userdata, msg):
        decoded_message=str(msg.payload.decode("utf-8"))
        print("on message")
        payload=json.loads(decoded_message)
        print(payload)
 
        if (msg.topic == "management" and payload["hostname"]==socket.gethostname()):

            if (msg.topic == "management" and payload["event"]=="sensorstart"):
                self.client.unsubscribe("management")
                x = threading.Thread(target=self.start_up(payload))
                x.start()
                
ToFSensor()