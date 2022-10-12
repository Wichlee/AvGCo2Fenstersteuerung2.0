import random
import time

from paho.mqtt import client as mqtt_client

# connect to remote test
broker = 'test.mosquitto.org'
port = 1883
topic = "AvG/controlunit"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


# connect routine
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Actor connected to MQTT Broker", broker, port)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# todo: Fallunterscheidung öffnen Fenster und schließen Fenster in on_message
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def open_actor():
    # Man würde normalerweise die Stellung des Servos anpassen um das Fenster zu öffen, aber print msg tuts auch...
    print("Actor now opening")


def close_actor():
    # Wir tun so als würde das Fenster einfach so schließen
    print("Actor now closing")


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
