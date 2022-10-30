import paho.mqtt.client as mqtt
import json
import time
import threading


class InitObject:

    def __init__(self):
        self.client = mqtt.Client()
        self.config = self.read_config()
        self.ip = '127.0.0.1'
        self.port = 1883

    def read_config(self):
        with open('config.json', 'r') as f:
            return f.read()

    def connect(self):
        self.client.connect(self.ip, self.port, 60)


class Device(InitObject):
    def __init__(self):
        super().__init__()

    def startup_message(self):
        self.connect()
        while True:
            self.client.publish('test', json.dumps({'message': 'startup'}))
            time.sleep(2)


class Manager(InitObject):
    def __init__(self):
        super().__init__()

    def on_message(self):
        self.client.publish('test', json.dumps({'message': 'from manager'}))

    def listen(self):
        self.connect()

        self.client.subscribe('test')
        self.client.on_message = self.on_message()


if __name__ == '__main__':
    d = Device()
    m = Manager()

    t1 = threading.Thread(target=d.startup_message)
    t2 = threading.Thread(target=m.listen)

    t1.start()
    t2.start()
