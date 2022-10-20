# Notes
Here's the service used to proof the validity of the pis and their data.

This contains a startup script which fires every time the device gets switched on. The `attest.py` listens for MQTT startup message.

Location of the script on the pi currently is `/usr/local/bin/startup_app.sh`

And the service is called `startup.check.service`. The file is located `/etc/systemd/system/startup.check.service`

## Installation

There is a small installation script which just moves two files to sepcific folders. After runnning the `sudo ./install.sh` script enable and start the service using systemd: 

```
sudo systemctl enable startup.check.service
sudo systemctl start startup.check.service
```

There is also a small script which restarts the daemon.
