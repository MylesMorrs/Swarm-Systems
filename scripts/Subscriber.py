import paho.mqtt.client as mqtt

ipAdress = input("Input IP Adress Of Mother: ")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Update callback API version
client._callback_api_version = 5  

client.connect('192.168.1.85', 1883, 60)
client.loop_forever()
