from multiprocessing.dummy import Manager
from device.Device import Device
from device.sensors.Sensor import Sensor
from device.Manager import Manager
import threading


def start():
    m = Manager()
    s = Sensor()

    t1 = threading.Thread(target=m.run)
    t2 = threading.Thread(target=s.start_up)
    t1.start()
    t2.start()


if __name__ == '__main__':
    start()
