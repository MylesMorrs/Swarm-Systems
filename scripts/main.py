import paho.mqtt.client as mqtt
import time
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

ip_address = get_ip_address()
print(f"My IP address is: {ip_address}")

# Use MQTTv5 for latest API
client = mqtt.Client(protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, reasonCode, properties):
    print("Connected with reason code", reasonCode)

client.on_connect = on_connect

client.loop_start()  # Start the network loop in a background thread

try:
    while True:
        client.publish("test/topic", "Hello from mother computer!")
        print("Message sent.")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()

