from abc import ABC, abstractmethod

class Sensor(ABC):
    
    def __init__(self):
        print("init")

    @abstractmethod
    def send_message(self):
        print("Sending message")

    def start_up():
        print("starting up generic sensor")
        
    @abstractmethod
    def measure_stuff(self):
        print("sensor specific implementation")
        ## sensor specific implementation

    

