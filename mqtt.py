from paho.mqtt import client as mqtt_client
import os

# Connect mqtt
def connect_mqtt():
    # Broker
    broker = os.getenv('BROKER')
    port = 1883

    # Id for client
    client_id = 'python-mqtt-SecuritySystem7000'

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    print(client)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


# Publishing
def publish(client, message):
    topic = "mqtt"
    msg = message
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
