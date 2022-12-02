import sys
sys.path.insert(0, '/opt/iot/secure_sensor_management_system')
from ExampleSensor.RngSensor import RngSensor


if __name__ == '__main__':
    x = RngSensor()
    x.run()
