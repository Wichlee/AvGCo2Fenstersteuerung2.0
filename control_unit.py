from random import randint
import time

from paho.mqtt import client as mqtt_client

# set broker parameters and topic
broker = 'test.mosquitto.org'
port = 1883
topic_co2level = "AvG/co2level"
topic_window_actor = "AvG/window_actor"
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
def publish_to_window(client, message):
    time.sleep(1)
    result = client.publish(topic_window_actor, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{message}`-window to topic `{topic_window_actor}`\n----")
    else:
        print(f"Failed to send message to topic {topic_window_actor}")


# subscription routine
def subscribe(client: mqtt_client):
    def on_message(client, userdata, message):
        if int(f"{message.payload.decode()}") > 2500:
            print(f"Received `{message.payload.decode()}` from `{message.topic}` topic\n~Too many aerosol particles!")
            publish_to_window(client, "open")
        else:
            print(f"Received `{message.payload.decode()}` from `{message.topic}` topic\n~Air quality is ok.")
            publish_to_window(client, "close")

    client.subscribe(topic_co2level)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
