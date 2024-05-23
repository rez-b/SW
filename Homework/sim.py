import paho.mqtt.client as mqtt
import numpy as np

broker = 'broker.emqx.io'
port = 1883
def simulate(Vx0, Vy0, T):
    t = np.arange(0, T+1)
    Vx = Vx0 - 9.8 * t
    Vy = Vy0 + t*0
    x = Vx0 * t - 0.5*9.8*t*t
    y = Vy0 * t
    return t, Vx, Vy, x, y

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        print('Send Vx0, Vy0, T for simulation')
        Vx0, Vy0, T = int(input()), int(input()), int(input())
        client.publish("t", str(simulate(Vx0, Vy0, T)[0]))
        client.publish("Vx", str(simulate(Vx0, Vy0, T)[1]))
        client.publish("Vy", str(simulate(Vx0, Vy0, T)[2]))
        client.publish("x", str(simulate(Vx0, Vy0, T)[3]))
        client.publish("y", str(simulate(Vx0, Vy0, T)[4]))
        print("Just published:\n" + str(simulate(50,10,10)[0]) +' to topic t')
        print(str(simulate(50,10,10)[0]) + ' to topic Vx')
        print(str(simulate(50,10,10)[2]) + ' to topic Vy')
        print(str(simulate(50,10,10)[3]) + ' to topic x')
        print(str(simulate(50,10,10)[4]) + ' to topic y')
    else:
        print("Failed to connect, return code %d\n", rc)
 
def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_forever()


if __name__ == '__main__':
    run()