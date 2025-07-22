import paho.mqtt.client as mqtt
import socket

client = mqtt.Client(protocol=mqtt.MQTTv5)

ip_address = "192.168.1.85"

def on_connect(client, userdata, flags, reasonCode, properties):
    print("Connected with reason code", reasonCode)
    client.subscribe("2")

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

def main():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(ip_address, 1883, 60)
    client.loop_start()  # Start the network loop in a background thread

    try:
        while True:
            client.publish("1", input("Enter message to publish: "))
            # print("Message sent.")
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()