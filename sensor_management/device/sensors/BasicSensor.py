from IoTElement import IoTElement
from datetime import datetime
import json


class BasicSensor(IoTElement):

    def __init__(self, n):
        super().__init__()
        self.sensor_name = n
        self.config["sensor"]["name"] = self.sensor_name
        self.config["event"] = "Sensor starting"
        self.config["message"] = "Sensor " + self.sensor_name + \
            " started on "+self.config["hostname"]
        self.config["sensor"]["timestamp"] = self.__get_time_stamp()
        self.config["timestamp"] = self.__get_time_stamp()
        self.client.publish("management", json.dumps(self.config))
        self.__attest_validate(self.config)

    def publish_data(self, data, topic_end):
        topic = "data/"+self.config["hostname"]+"/sensor/"+topic_end
        self.client.publish(topic, payload=data)

    def __attest_validate(self, json_update):
        json_object = json_update
        # Needs to specify the event type
        json_object["event"] = "validateSensor"
        json_object["message"] = "Sensor validation request"
        json_object["timestamp"] = self.__get_time_stamp()
        print(json_object)
        # Publish to manager for validation
        self.client.publish(f"management", json.dumps(json_object))

    def __get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time
