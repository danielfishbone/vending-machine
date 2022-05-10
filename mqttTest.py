#!python3

import paho.mqtt.client as mqtt 
import time 

def on_message(client,userdata,msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8","ignore"))
    print("message received ", m_decode)

def on_log(client,userdata,level,buf):
    print("log: "+buf)
def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("connected ok")
    else:
        print("bad connection return code = ",rc)  
def on_disconnect(client,userdata,flags,rc=0) :
    print("Diconnected result code"+ str(rc) )

broker = "test.mosquitto.org"

client = mqtt.Client("pythonq")
client.on_connect = on_connect
client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_message = on_message
print("connecting to broker",broker)
client.connect(broker)
client.loop_start()
client.subscribe("house/sensor1")

# client.publish("house/sensor1","Hello world!")
time.sleep(10)
client.subscribe("house/sensor1")

client.loop_stop()
client.disconnect()