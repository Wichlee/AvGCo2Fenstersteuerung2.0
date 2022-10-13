import random

from paho.mqtt import client as mqtt_client

# connect to remote test
broker = 'test.mosquitto.org'
port = 1883
topic = "AvG/window_actor"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
window_open: bool = False


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


# Printing the actual window status
def print_status(status):
    print(f"Is the window now open? {status}\n----")


# Mocking the opening process of the window actor
def open_window():
    window_open = True
    print_status(window_open)


# Mocking the closing process of the window actor
def close_window():
    window_open = False
    print_status(window_open)


# deciding whether to open or close the window actor by checking the message and the current window status
def decide(message):
    if message == "open":
        if not window_open:
            open_window()
    else:
        close_window()


# subscription routine
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}`-window from topic `{msg.topic}`")
        decide(msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
