from random import randint
import time

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import Client

# set broker parameters and topic
broker = 'test.mosquitto.org'
port = 1883
topic_co2level = "AvG/co2level"
topic_actorwindow = "AvG/actorwindow"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{randint(0, 1000)}'


# connect routine
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Controller connected to MQTT Broker", broker, port)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# publish routine
def publish_window_actor(client):
    while True:
        time.sleep(1)
        subscribe(client)
        result = client.publish(topic_actorwindow, subscribe(client))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{subscribe(client)}` to topic `{topic_actorwindow}`")
        else:
            print(f"Failed to send message to topic {topic_actorwindow}")
        time.sleep(10)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # return msg.payload.decode()

    client.subscribe(topic_co2level)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    # publish_window_actor(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
