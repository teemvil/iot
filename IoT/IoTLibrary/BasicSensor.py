from IoTLibrary.IoTElement import IoTElement
import json
import argparse


class BasicSensor(IoTElement):

    def __init__(self):
        super().__init__()

        self.sensor_config = self.read_config_from_argument()

        self.sensor_name = self.sensor_config["name"]
        self.frequency = self.sensor_config["frequency"]

        self.message["sensor"]["name"] = self.sensor_name
        self.message["event"] = "Sensor starting"
        self.message["message"] = "Sensor " + self.sensor_name + \
            " started on "+self.message["device"]["hostname"]
        self.message["sensor"]["starttimestamp"] = self.get_time_stamp()
        self.message["messagetimestamp"] = self.get_time_stamp()
        self.client.publish("management", json.dumps(self.message))
        # self.attest_validate(self.message)

    def publish_data(self, data, topic_end):
        topic = f"{self.sensor_config['prefix']}/{topic_end}"
        self.client.publish(topic, payload=data)

    def run(self):
        pass

    def attest_validate(self, json_update):
        json_object = json_update
        # Needs to specify the event type
        json_object["event"] = "validateSensor"
        json_object["message"] = "Sensor validation request"
        json_object["messagetimestamp"] = self.get_time_stamp()
        print(json_object)
        # Publish to manager for validation
        self.client.publish(f"management", json.dumps(json_object))

    def read_config_from_argument(self):
        all_args = argparse.ArgumentParser()
        all_args.add_argument("-f", "--config", type=argparse.FileType("r"),  required=True,
                              help="Config file to be used.")

        args = vars(all_args.parse_args())
        return json.loads(args["config"].read())
