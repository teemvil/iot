from tofSensor import ToFSensor
import threading
import json


def start():
    s = ToFSensor(1, "tof")
    #s.__init__(1, "tof")
    s.measure_stuff()
    #t1 = threading.Thread(target=s.measure_stuff())
    #t2 = threading.Thread(target=s.start_up)
    
   


if __name__ == '__main__':
    start()
