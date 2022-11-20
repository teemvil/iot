from .IoTElement import IoTElement
import json
import time

class Device(IoTElement):
    def __init__(self):
        super().__init__()
        
        self.device_config = self.read_config("device.json")
        self.itemid = self.device_config["itemid"]
        self.hostname = self.device_config["hostname"]
        self.event = self.device_config["event"]
        self.message = self.device_config["message"]
        self.address = self.device_config["address"]
        self.timestamp = self.device_config["timestamp"]
        
        self.startup()
        
        try:
            while True:
                #self.client.publish("management", json.dumps({'message': 'doing stuff'}))
                print("doing stuff")
                time.sleep(1)
        except:
            print("Exception during while loop, exiting...")
            self.client.loop_stop()
            self.client.disconnect()
                

    def startup(self):
        self.client.subscribe("management")
        self.client.on_message = self.on_message
        self.client.loop_start()
        self.client.publish('management', json.dumps({"itemid":self.itemid, "address": self.address, "hostname": self.hostname, "event": self.event , 'message': self.message, "timestamp": self.timestamp}))
        
    def on_message(self, client, nonetype, msg):
        print(f"Received message with topic: '{msg.topic}' and message: '{msg.payload.decode()}'")
    
    