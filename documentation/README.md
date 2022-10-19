documentation to be filled in...

# Setup

## Requirements

- one or more raspberry pi
- one or more sensors

In this project we used three raspberry pi devices. Sensors in use were IR-sensor, lux-sensor and time of flight-sensor. We also used a web-camera.

## Connecting sensors for pi

Tutorials for different kinds of raspberry pi sensors:
https://tutorials-raspberrypi.com/raspberry-pi-sensors-overview-50-important-components/

//images here if needed

We connected the lux-sensor and web-camera to one raspberry pi. The IR-sensor and time of flight-sensor were connected separately on remaining two raspberry pi devices.

## Required software for pi

Each raspberry pi needs a bootup file script that uses the systemd.

- Python3
- vim or nvim if you don't want to use nano
- mqtt
- flask (attestation, web-camera, REST)
- Imports from sensor manufacturer (board, busio etc.)

##
