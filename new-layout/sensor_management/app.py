from multiprocessing.dummy import Manager
from device.Device import Device
from device.sensors.Sensor import Sensor
from device.Manager import Manager
import threading

def start():
    s = Sensor
    d = Device(s)
    m = Manager()

    t1 = threading.Thread(target=d.startup_message)
    t2 = threading.Thread(target=m.listen)
    t1.start()
    t2.start()

    

if __name__ == '__main__':
    start()