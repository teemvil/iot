from initObject import InitObject
import socket
import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime


class NewSensor(InitObject):
    
    def __init__(self):
        super().__init__()
        payload = self.config
        IP = self.config["client"]["host"]
        PORT = self.config["client"]["port"]    
        self.connect()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()
		
    def start_up(self, json_load):
        payload = json_load
        payload["message"]= "New sensor started on device"
        payload["event"]="sensoronline"
        payload["sensor"]["timestamp"]=self.get_time_stamp()
        payload["sensor"]["name"]="NewSensor"
        self.send_message(payload)
        self.measure_stuff(payload)
    
    def measure_stuff(self, json_object):
        payload=json_object
        payload["message"]= "New Sensor sensor running on device"
        payload["event"]="sensorrunning"
        self.send_message(payload)  
        payload["message"]="New Sensor sensor trasmitting data"
        payload["event"]="sensortrasmitting"
        self.send_message(payload) 
		
        ## Write your sensor's measurement code here!!

        ##  while True:
        ## 	  self.client.publish("random", payload=(random.random())
        ## 		time.sleep(1)        

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
