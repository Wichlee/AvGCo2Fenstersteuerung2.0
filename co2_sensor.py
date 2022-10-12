from random import randint
import time

from paho.mqtt import client as mqtt_client

# set broker parameters and topic
broker = 'test.mosquitto.org'
port = 1883
topic = "AvG/co2level"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{randint(0, 1000)}'


# connect routine
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker", broker, port)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# publish routine
def publish(client):
    while True:
        time.sleep(1)
        randNumber = int(randint(1000, 3500))
        result = client.publish(topic, randNumber)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{randNumber}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(2)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
