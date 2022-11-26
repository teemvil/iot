from IoTLibrary.Device import Device
import paho.mqtt.client as mqtt


def start():
    d = Device()
    d.startup()


if __name__ == '__main__':
    start()
