import paho.mqtt.client as mqtt

ip_address = input("Input IP Address Of Mother (broker): ")

def on_connect(client, userdata, flags, reasonCode, properties):
    print("Connected with reason code", reasonCode)
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

# Use the CallbackAPIVersion enum
client = mqtt.Client(protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip_address, 1883, 60)
client.loop_forever()
