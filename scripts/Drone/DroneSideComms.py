import paho.mqtt.client as mqtt
import socket
import time
import Config  
from Config import id

client = mqtt.Client(protocol=mqtt.MQTTv5)
ip_address = "192.168.1.85"

RECONNECT_DELAY = 1
MAX_RECONNECT_COUNT = 60

newid = False

def update_config_id(new_id):
    lines = []
    with open('Config.py', 'r') as file:
        for line in file:
            if line.strip().startswith('id ='):
                lines.append(f"id = '{new_id}'\n")
            else:
                lines.append(line)
    with open('Config.py', 'w') as file:
        file.writelines(lines)

def on_connect(client, userdata, flags, reasonCode, properties):
    print("Connected with reason code", reasonCode)
    client.publish("config", id)
    if id == '0000':
        newid = True
    # Subscribe to the topics you want to listen to
    client.subscribe([
        ("drone/config", 0),
        ("all/alert", 0)
        ])

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0
    while reconnect_count < MAX_RECONNECT_COUNT:
        print("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print("Reconnected successfully!")
            return
        except Exception as err:
            print("%s. Reconnect failed. Retrying...", err)

        reconnect_count += 1
    print("Reconnect failed after %s attempts. Exiting...", reconnect_count)



def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")
    topic = msg.topic
    payload = msg.payload.decode()

    # Only handle messages from a specific topic
    if topic == "drone/config":
        if payload.startswith("mother ") and newid:
            try:
                new_id = int(payload.split()[1])
                # Set the drone's ID variable here
                print(f"Drone ID updated to: {new_id}")
                update_config_id(new_id)
                newid = False
            except (IndexError, ValueError):
                print("Invalid ID format received.")
   # Ignore any other topics
    else:
        pass

def main():
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        client.connect(ip_address, 1883, 60)
    except Exception as e:
        print(f"Failed to connect to MQTT broker at {ip_address}: {e}")
        return

    client.loop_start()  # Start the network loop in a background thread

    try:
        while True:
            message = input("Enter message to publish: ")
            if message.lower() == 'exit':
                break
            client.publish("1", message)
            print("Message sent.")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()