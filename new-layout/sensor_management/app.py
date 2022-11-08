import time
import paho.mqtt.client as mqtt


class ClientState():
    # This is the InitObject. Renamed just to make it more clear what this does.
    # All the configuration should be stored here.
    # All the configs could also be stored in config file and just read at
    # creation time.
    def __init__(self):
        # All the necessary mqtt-client info. All the child classes inherit these.
        self.config = {
            'ip': '127.0.0.1',
            'port': 1883,
            'keepalive': 60
        }
        self.client = mqtt.Client()

    def connect(self):
        # Connect to mqtt broker. Ip and stuff is read from config file.
        # ip = self.config.get('ip')
        # print(f'connected to broker at {ip}')
        response = self.client.connect(self.config.get('ip'), self.config.get(
            'port'), self.config.get('keepalive'))
        return response

    def publish(self, topic, payload):
        # Publish stuff to the broker.
        # print(f'published message to {topic} with payload {payload}')
        info = self.client.publish(topic, payload)
        return info

    def subscribe(self, topic):
        # Subscribe to the mqtt broker. How the different topics are handled
        # needs to be decided.
        # print(f'subscribed to topic {topic}')
        return_value = self.client.subscribe(topic)
        return return_value


class Sensor(ClientState):
    def __init__(self):
        super().__init__()
        self.connect()
        self.sensor_startup('sensorn start')

    def sensor_startup(self, payload):
        # Publish message to the mqtt broker using ClientState.
        # print(f'Hello from sensor {payload}')
        self.publish('data', payload)

    def run(self):
        self.measure()
        print(self.data)


class Manager():
    def __init__(self, sensor):
        self.sensor = sensor
    
    def listen_for_changes(self, value):
        self.sensor.data = value


class SensorN(Sensor):
    def __init__(self):
        super().__init__()
        self.data = '12345'
        self.manager = Manager()

    def measure(self):
        # This is all that needs to be configured by the user.
        i = 0
        while True:
            self.publish('data', i)
            time.sleep(5)
            i += 1


if __name__ == '__main__':
    # How to change this. Parameterize?
    x = SensorN()
    x.run()
