from IoTElement import IoTElement
import json
import threading
import random


class BasicSensor(IoTElement):

    def __init__(self, n):
        super().__init__()
        self.sensor_name = n        
        self.config["sensor"]["name"]= self.sensor_name
        self.config["event"]="Sensor starting"
        self.config["message"] = "Sensor "+ self.sensor_name +" started on "+self.config["hostname"]
        self.client.publish("management", json.dumps(self.config))

    def publish_data(self, data, topic_end):
        topic = "data/"+self.config["hostname"]+"/sensor/"+topic_end
        self.client.publish(topic, payload=data)

