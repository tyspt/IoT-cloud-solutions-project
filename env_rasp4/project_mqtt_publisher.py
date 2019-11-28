from datetime import datetime

import paho.mqtt.client as paho
import ssl
import time
import logging

import credential as cr

''' MQTT helper class that provides functions to connect to server using preset information on credential.py
    and to publish data under a given topic. The programm should be able to handle disconnection automatically 
    all by itself.
'''


class MQTTDataPublisher:
    def __init__(self):
        self.client = paho.Client()  # create client object
        self.client.isConnected = False

        # set username and password
        self.client.username_pw_set(username=cr.username, password=cr.password)

        # handle SSL encryption if enabled in credential.py settings
        if cr.isSSLEnabled:
            self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                                tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            self.client.tls_insecure_set(False)

        # binding callback functions
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

        # main mqtt event loop
        self.client.loop_start()

        # try to connect to server at first start up
        while not self.client.isConnected:
            try:
                logging.info("(MQTT) ............ connecting ............")
                # establish connection
                self.client.connect(
                    host=cr.broker, port=cr.port, keepalive=60, bind_address="")
            except:
                logging.info(
                    "(MQTT) Failed to establish connection to server, retrying...")
            
            time.sleep(3)

    def on_publish(self, cl, userdata, result):  # create function for callback
        logging.info("(MQTT) data published " + str(userdata))
        pass

    def on_connect(self, cl, userdata, flags, rc):
        if rc == 0:
            logging.info("(MQTT) Successfully connected")
            self.client.isConnected = True
        else:
            logging.info("(MQTT) Bad connection, RC = ", rc)
            self.client.isConnected = False

    def on_disconnect(self, cl, userdata, rc):
        if rc == 0:
            logging.info(
                "(MQTT) Programm disconnectes from server, waiting to exit...")
            cl.loop_stop()
        else:
            logging.error(
                "(MQTT) Unexpected disconnection, trying to reconnect...")
            self.client.isConnected = False

    # This is the function that publishes data to cloud
    def publish_data_to_cloud(self, topic, data):
        self.client.user_data_set({topic: data})
        self.client.publish(topic, data)  # publish

    # stop the loop when exiting the script
    def disconnect(self):
        self.client.disconnect()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
                        level=logging.DEBUG)
    mqtt = MQTTDataPublisher()
    mqtt.publish_data_to_cloud("Hello World", "test")
    
    time.sleep(5)
    mqtt.publish_data_to_cloud("Hello World", "test")
    
    time.sleep(5)
    mqtt.publish_data_to_cloud("Hello World", "test")

    input("")
