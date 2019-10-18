import paho.mqtt.client as paho
import credential as cr
import ssl

def on_publish(client, userdata, result):  # create function for callback
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish(
        "test", "test123")  # publish


client = paho.Client()  # create client object
client.username_pw_set(username=cr.username, password=cr.password)

if cr.isSSLEnabled:
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    client.tls_insecure_set(False)

client.on_connect = on_connect
client.on_publish = on_publish  # assign function to callback

client.connect(cr.broker, cr.port)  # establish connection

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()