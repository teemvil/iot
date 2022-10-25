from Lux_subclass import LuxSensor
from device import Device

# function to test if parameter base class is Device
def base_test(sensor):
    if sensor.__class__.__bases__[0] == Device:
        print("Base class is Device")

def main():
    LuxSensor.send_message()
    test = LuxSensor()
    test.measure_stuff()
    #test2 = LuxSensor()
    #arr = [test, test2]
    
    #testivar = "22"
    #print(testivar.__class__.__bases__[0])
    
    #base_test(testivar)
    #base_test(test)
    #base_test(test2)
    #print(arr)
    
    #shows the base class
    #print(test.__class__.__bases__[0])
    
    #print(Device)
    
if __name__ == "__main__":
    main()
