import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("localhost", 1883, 60)
while True:
    try:
        client.publish("test/topic", "Hello from mother computer!")
        print("Message sent.")
        time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        break

