# Notes
Here's the service used to proof the validity of the pis and their data.

This contains a startup script which fires every time the device gets switched on. The `attest.py` listens for MQTT startup message.

Location of the script on the pi currently is `/usr/local/bin/startup_app.sh`

And the service is called `startup.check.service`. The file is located `/etc/systemd/system/startup.check.service`

## Some notes

Startup check should fire MQTT event and then start a second process which is the device manager type of an app. This should be something like this (in pseudocode):

```
connect_to_mqtt_client()

publish_mqtt_message()

everything_is_fine = listen_to_mqtt_attest_fine_message()

if everything_is_fine:
  os.start(path_to_the_device_manager)
else
  publish_alert_message()

```

## Installation

There is a small installation script which just moves two files to sepcific folders. After runnning the `sudo ./install.sh` script enable and start the service using systemd: 

```
sudo systemctl enable startup.check.service
sudo systemctl start startup.check.service
```

There is also a small script which restarts the daemon.
