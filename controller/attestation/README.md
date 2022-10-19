# Notes
Here's the service used to proof the validity of the pis and their data.

This contains a startup script which fires every time the device gets switched on. The `attest.py` listens for MQTT startup message.

Location of the script on the pi currently is `/usr/local/bin/startup_app.sh`

And the service is called `startupCheck.service`. The file is located `/etc/systemd/system/startupCheck.service`

