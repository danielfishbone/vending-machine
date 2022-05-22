import os
import paho.mqtt.client as mqtt
import configparser

from time import sleep



config = configparser.ConfigParser()
start_top = "machine/startapp"
broker = "test.mosquitto.org"
port = 1883


def on_connect(client,userdata,flags,rc): 
    print("Connected - rc:",rc)    
    
def on_subscribe(client, userdata,mid,granted_qos):
    print("Subscribed:", str(mid),str(granted_qos))

def on_unsubscirbe(client,userdata,mid):
    print("Unsubscribed:",str(mid))

def on_disconnect(client,userdata,rc):
    if rc !=0:
        print("Unexpected Disconnection")

def on_message(client,userdata,message):
    global start_top

    print(("message recieved"))
    print(str(message.payload.decode("utf-8")))
    if str(message.topic)== start_top:
        os.system('./app.py')

config.read('.config.ini')
broker = config.get('DEFAULT', 'broker',fallback = 'test.mosquitto.org' )  

client = mqtt.Client("client4152")
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker,port)

sleep(1)
client.loop_start()
client.subscribe('machine/startapp')

os.system('python3 app.py')
sleep(2)

while 1:
    run = True