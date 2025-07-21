
Drone Swarm System - Communication Architecture
===============================================

System Overview
---------------
Mother Drone:
- Coordinates all drones.
- Receives video and sensor data for situational awareness.
- Runs MQTT broker (Mosquitto) for communication.
- Displays telemetry and video feeds via GUI.

Drones:
- Raspberry Pi Zero with RTK GPS (~2cm accuracy).
- Publishes GPS data to flight controller at ~5Hz.
- Sends Ardupilot MAVLink commands (Takeoff, Land, Waypoint).


Communication Breakdown
------------------------

Normal Communication (Telemetry & Commands):
- Protocol: MQTT
- Payload: MAVLink messages
- Broker: Mosquitto on Mother computer

Video Communication (One-way):
- Protocol: GStreamer over UDP (Unicast)
- Encoding: H.264
- Framerate Goal: 10-15 FPS
- Resolution: Center-cropped; minimal viable resolution
- Direction: Drone --> Mother only


Required Packages
-----------------

Python Packages (both sender & receiver):
    pip install paho-mqtt
    pip install PyGObject (Only Works On Linux Systems)
    pip install dearpygui

Linux (Mother / Receiver) System Packages:
    sudo apt update
    sudo apt install python3-gi python3-gi-cairo gir1.2-gst-plugins-base-1.0 \
        gir1.2-gstreamer-1.0 gstreamer1.0-tools \
        gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
        gstreamer1.0-plugins-ugly gstreamer1.0-libav

Windows (Drone / Sender) Setup for GStreamer:
---------------------------------------------
1. Download and install GStreamer Full Runtime (MSVC 64-bit) from:
   https://gstreamer.freedesktop.org/download/#windows

2. Ensure these directories are added to your Windows PATH:
   C:\gstreamer\1.0\x86_64\bin
   C:\gstreamer\1.0\x86_64\lib\gstreamer-1.0
		Press Windows + S then search for enviromental variables
		click the one labeled path and press edit
		create new and upload path for above files (Create new for each file path)

3. Restart MSYS2 MinGW 64-bit terminal after updating PATH.

4. Confirm plugins are available:
    - Run in cmd or PowerShell:
      gst-inspect-1.0 ksvideosrc

5. Test video input:
    gst-launch-1.0 ksvideosrc ! autovideosink

6. For your Python pipeline, use ksvideosrc with device-name set to "Integrated Camera".


Useful Docs & References
-------------------------
GUI:    https://dearpygui.readthedocs.io/en/latest/documentation/themes.html
MQTT:   https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html
RTK GPS: https://www.waveshare.com/wiki/LC29H(XX)_GPS/RTK_HAT


Project Idea Summary
--------------------
- Central "Mother" computer for coordination and monitoring.
- Drones report GPS + low-bandwidth video.
- Lightweight, low-latency stack: MQTT + UDP Video.
- Ready for future swarm behaviors and autonomy.
