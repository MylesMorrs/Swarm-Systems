Idea:
	Have one "Mother" computer that talks to the drones and coordinates everything.
	
	Would be nice if mother can receive video and sensor data to have a better understanding of the environment.
	
	On each drone we will have a raspberry pi zero with a RTK GPS (~2cm). The raspberry pi will get the GPS coordinates
	and publish to the drone at about 5 times a second (Max RTX gps refresh rate). Along with the GPS info it will send Ardupilot 
	(Running on the flight controller) commands like "Take off", "Land", and "Go to this way point"

Normal communication:
	MQTT with MAVLink underneath
	Mother run Mosquitto 
	
Video communication:
	GStreamer over UDP (Unicast)
		Video compressed with h.264
			center based video resolution  
		Keep resolution down to min possible
		Goal of 10-15 FPS
test