import paho.mqtt.client as mqtt
import credential as cr
import ssl

topic = "#"

# The callback for when the client receives a CONNACK response from  # the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
# Subscribing in on_connect() means that if we lose the
# connection and reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


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
