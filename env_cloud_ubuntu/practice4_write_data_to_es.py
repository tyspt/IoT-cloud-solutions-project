# from datetime import datetime
# from elasticsearch import Elasticsearch
# es = Elasticsearch()

# doc = {
#     'temperature': 17,
#     'time': datetime.now()
# }
# res = es.index(index="temp", doc_type='_doc', id=4, body=doc)
# print(res['result'])



import paho.mqtt.client as mqtt
from datetime import datetime
import credential as cr
import ssl, time

# topic = "oth/tony/sensor/temperature"
topic = "#"

# The callback for when the client receives a CONNACK response from  # the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the
    # connection and reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(str(datetime.now()) + ": " + msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.username_pw_set(username=cr.username, password=cr.password)

if cr.isSSLEnabled:
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                   tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    client.tls_insecure_set(False)

client.on_connect = on_connect
client.on_message = on_message

client.connect(cr.broker, cr.port)

# Blocking call that processes network traffic, dispatches callbacks # and handles reconnecting.
client.loop_forever()
