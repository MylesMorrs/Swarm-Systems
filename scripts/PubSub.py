import paho.mqtt.client as mqtt
import socket

client = mqtt.Client(protocol=mqtt.MQTTv5)

ip_address = input("Input IP Address Of Mother (broker): ")

def on_connect(client, userdata, flags, reasonCode, properties):
    print("Connected with reason code", reasonCode)

client.on_connect = on_connect

client.connect(ip_address, 1883, 60)
client.loop_start()  # Start the network loop in a background thread

try:
    while True:
        client.publish("test/topic", input("Enter message to publish: "))
        # print("Message sent.")
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()