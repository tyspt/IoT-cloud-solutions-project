import paho.mqtt.client as mqtt
from datetime import datetime
from elasticsearch import Elasticsearch

import credential as cr
import global_config as config 
import ssl, time, json

# The callback for when the client receives a CONNACK response from  # the server.
def on_connect(client, userdata, flags, rc):
    print(str(datetime.now()) + ": Connected with result code " + str(rc))

    topic = config.TOPIC_PREFIX_SENSOR + "#"
    client.subscribe(topic)
    print(str(datetime.now()) + ": Subscribed to topic " + topic)

# All the processing logic after receiving a message is written in the functioon here
def on_message(client, userdata, msg):
    # print(str(datetime.now()) + ": " + msg.topic+" "+str(msg.payload))
    sub_topic = msg.topic.split(config.TOPIC_PREFIX_SENSOR)[1]
    
    unit = sub_topic.split('/')[1]
    sub_topic  = sub_topic.split('/')[0]

    value = float(msg.payload)
    print(value)
    
    if value is not None:
        doc = {}
        doc['topic'] = str(msg.topic)
        doc[sub_topic] = value
        doc['unit'] = unit
        doc['time'] = datetime.utcnow()

        # print(doc)
        es_index = 'project_aquaponics_' + sub_topic
        res = es.index(index=es_index, doc_type='_doc', body=doc)
        print(str(datetime.now()) + ": " + str(res['result']) +" under index: " + es_index + ", data: " + str(doc) )

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
