import paho.mqtt.client as mqtt

broker = 'broker.emqx.io'
port = 1883

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("Vx")
        client.subscribe("Vy")
        client.subscribe("x")
        client.subscribe("y")
        client.subscribe("t")
    else:
        print("Failed to connect, return code %d\n", rc)
   
def on_message(client, userdata, message):
    print("Recieved data in topic " + message.topic + str(message.payload))
    with open("data.txt", "a") as file:
        file.write(f"{message.topic}: {message.payload}\n")

def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_forever()


if __name__ == '__main__':
    run()