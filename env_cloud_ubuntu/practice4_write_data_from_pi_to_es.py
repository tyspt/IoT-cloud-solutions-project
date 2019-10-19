import paho.mqtt.client as mqtt
from datetime import datetime
from elasticsearch import Elasticsearch

import credential as cr
import ssl, time, json

# set up topic
TOPIC_PREFIX = "oth/tony/db/rasp_1/sensor/"
topic =  TOPIC_PREFIX + "#"

# topic = "oth/tony/status/rasp_1/state"

# The callback for when the client receives a CONNACK response from  # the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    # print(str(datetime.now()) + ": " + msg.topic+" "+str(msg.payload))
    sub_topic = msg.topic.split(TOPIC_PREFIX)[1]
    # print(sub_topic)

    value = str(msg.payload.decode("utf-8","ignore"))
    # print(value)
    
    if value is not None:
        new_index_id = None
        try:
            new_index_id = es.count(index=sub_topic, doc_type='_doc')["count"] + 1
        except:
            new_index_id = 1
        print(new_index_id)

        doc = {}
        doc[sub_topic] = value
        doc['time'] = datetime.now()

        # print(doc)

        res = es.index(index=sub_topic, doc_type='_doc', id=new_index_id, body=doc)
        # print(res['result'])

# create instance for elasticsearch
es = Elasticsearch()

# mqtt instance
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
