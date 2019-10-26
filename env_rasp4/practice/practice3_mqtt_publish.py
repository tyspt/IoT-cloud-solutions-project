import paho.mqtt.client as paho
from sense_hat import SenseHat
from datetime import datetime
import credential as cr
import ssl, time


def on_publish(client, userdata, result):  # create function for callback
    print(str(datetime.now()) + ": data published")
    pass

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK")
    else:
        print("Bad connection, RC = ", rc)
    
    
client = paho.Client()  # create client object

client.username_pw_set(username=cr.username, password=cr.password)

if cr.isSSLEnabled:
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    client.tls_insecure_set(False)

client.on_connect = on_connect
client.on_publish = on_publish  # assign function to callback

try:
    client.connect(cr.broker, cr.port)  # establish connection
    
    sense = SenseHat()
    sense.clear()
    
    client.publish("oth/tony/sensor", "Im going to publish sensor data now.")  # publish
    
    # send out Temperature, Pressure and Humidity
    while True:
        pressure = sense.get_pressure()
        temp = sense.get_temperature()
        humidity = sense.get_humidity()

        client.publish("oth/tony/sensor/pressure", pressure)  # publish
        client.publish("oth/tony/sensor/temperature", temp)  # publish
        client.publish("oth/tony/sensor/humidity", humidity)  # publish

        time.sleep(3)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
except:
   print("Failed to connect") 
finally:
    client.loop_stop()
    print("exiting...")