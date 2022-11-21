from device.IoTElement import IoTElement
from datetime import datetime
import json
import pathlib


class BasicSensor(IoTElement):

    def __init__(self):
        super().__init__()
        path = pathlib.Path(__file__).resolve().parent
        self.sensor_config = self.read_config_file(
            f"{path}/sensor_config.json")
        self.sensor_name = self.sensor_config["name"]
        self.frequency = self.sensor_config["frequency"]
        self.topic_end = self.sensor_config["topic_end"]

        self.message["sensor"]["name"] = self.sensor_name
        self.message["event"] = "Sensor starting"
        self.message["message"] = "Sensor " + self.sensor_name + \
            " started on "+self.message["device"]["hostname"]
        self.message["sensor"]["timestamp"] = self.__get_time_stamp()
        self.message["timestamp"] = self.__get_time_stamp()
        self.client.publish("management", json.dumps(self.message))
        self.__attest_validate(self.message)

    def publish_data(self, data, topic_end):
        topic = "data/"+self.message["hostname"]+"/sensor/"+topic_end
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
