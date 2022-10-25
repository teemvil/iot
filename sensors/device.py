from abc import ABC, abstractmethod

class Device(ABC):
    ip: str
    port: int
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    @abstractmethod
    def send_message(self):
        pass
        
    @abstractmethod
    def measure_stuff(self):
        pass

    def start_up(self):
        print("starting up generic sensor")

    

