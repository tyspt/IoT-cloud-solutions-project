import paho.mqtt.client as paho
from sense_hat import SenseHat
from datetime import datetime
import credential as cr
import ssl, time

TOPIC_PREFIX = "/iot_cloud_solutions/practice/db/regensburg/rpi_1/sensor/"
SLEEP_TIME = 3

sense = SenseHat()
sense.clear()

client = paho.Client()  # create client object
client.isConnected = False

def on_publish(cl, userdata, result):  # create function for callback
    print(str(datetime.now()) + ": (Callback) data published")
    pass


def on_connect(cl, userdata, flags, rc):
    if rc == 0:
        print(str(datetime.now()) + ": (Callback) Successfully connected")
        client.isConnected = True
    else:
        print(str(datetime.now()) + ": (Callback) Bad connection, RC = ", rc)
        client.isConnected = False


def on_disconnect(cl, userdata, rc):
    if rc == 0:
        print(str(datetime.now()) + ": (Callback) Programm disconnectes from server, waiting to exit...")
        cl.loop_stop()
    else:
        print(str(datetime.now()) + ": (Callback) Unexpected disconnection, trying to reconnect...")
        client.isConnected = False




client.username_pw_set(username=cr.username, password=cr.password)

# handle SSL encryption if enabled in credential.py settings
if cr.isSSLEnabled:
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                   tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    client.tls_insecure_set(False)

# binding callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect 

# main mqtt event loop
client.loop_start()

# try to connect to server at first start up
while not client.isConnected:
    try:
        client.connect(host=cr.broker, port=cr.port, keepalive=60, bind_address="")  # establish connection
    except:
        print(str(datetime.now()) + ": (MainThread) Failed to establish connection to server, retrying...")
        time.sleep(SLEEP_TIME)

# send out Temperature, Pressure and Humidity
try:
    while True:
        # print(str(client.isConnected))
        while not client.isConnected:
            print(str(datetime.now()) + ": (MainThread) Not connected... waiting for connection...")
            time.sleep(SLEEP_TIME)

        pressure = sense.get_pressure()
        temp = sense.get_temperature()
        humidity = sense.get_humidity()

        client.publish(TOPIC_PREFIX + "pressure", pressure)  # publish
        client.publish(TOPIC_PREFIX + "temperature", temp)  # publish
        client.publish(TOPIC_PREFIX + "humidity", humidity)  # publish

        # senseHat flashes once it sends out a set of measure data
        sense.clear((50, 50, 50))
        time.sleep(0.05)
        sense.clear((0, 0, 0))

        time.sleep(SLEEP_TIME)
except:
    pass
finally:
    # stop the loop when exiting the script
    client.disconnect()
    print("Exiting script...")
