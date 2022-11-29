# Intro

This is repository of a innovation project done for Nokia. The idea is to build a framework which allows rapid development of different kinds of sensor management systems. The sensor could ultimately be anything. 

The data aquisiton functionality is being abstracted so that the system doesn't need to know what kind of a sensor has been attached to it.

The system handles all communication via MQTT messages. 

# Installation

1.  a) Go to the folder /opt/ on the terminal

    b) Clone the repository using git: `sudo git clone https://github.com/teemvil/iot.git`. This downloads all the necessary library files.
    
    c) cd to the install folder `cd iot/install` and run the installation script: 
    ```
    sudo python3 install.py
    ```

    The script creates iot.devices.service and iot.sensors.service files to etc/systemd/system. The script also creates two config files to `etc/iotDevice/` these are used as MQTT client configuration and as a specific device configuration. The device configuration file should contain the itemid of the pi on which the scripts are running on.
    
    d) Enable the services using systemd:

    ```
    sudo systemctl enable iot.devices.service
    sudo systemctl start iot.devices.service
    ```

    ```
    sudo systemctl enable iot.sensors.service
    sudo systemctl start iot.sensors.service
    ```

2. Create sensor/implementations 

    a) Create a new folder for the sensor under /opt/iot/    

    b) Copy our SensorTemplate.py and sensor_config_template.json files there    

    c) Change the templates to fit your specific sensor needs    

    d) Add your new sensor to IotSensorStartup.py so that it can be started

        # from YourNewSensor import YouNewSensor
        # x = YourNewSensor()
        # x.run()

3. Reboot your machine OR run the IotSensorStartup.py script on a terminal to get the sensor operating


# Design

The system is build so that every class inherits a MQTT client from the IoTElement class. There is also a configuration file located in xxx which has all the necessary options to connect to the MQTT broker and send correct types of messages.

![device class diagram](documentation/pics/insidedevice.JPG)

# Data flow

When the system starts up it sends various MQTT messages to notify the broker about the state of the various subsystems. Firstly the validity of the device running the sensor script is checked. The sensor startup doesn't depend on the validity check. We can just see if the device is valid or not. 

![sequence diagram](documentation/pics/devicesequence.JPG)

## MQTT topic naming conventions

Sensors are named as `sensor/webcam`, `sensor/ir`, `sensor/lux`, `sensor/tof`.

### Management channel
```
management/
```

### Alert channel
```
alert/
```

### Data channels
```
data/<hostname>/<sensor>/<measurement>
```
Measurement here means the measured data. This could be array of pixels, temperature, distance etc


Most important payload fields:
itemid and event

Document the different events:
"device start up", "sensor start up", "platform? start up", etc...
