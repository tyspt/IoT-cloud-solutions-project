from datetime import datetime

import paho.mqtt.client as paho
import ssl
import time
import logging

import credential as cr
import project_device_control as control

''' MQTT helper class that provides functions to connect to server using preset information on credential.py
    and to publish data & retrive data under a given topic. The programm should be able to handle disconnection
    automatically all by itself.
'''


class MQTTDataHelper:
    def __init__(self, subscriber_topic):
        self.client = paho.Client()  # create client object
        self.client.isConnected = False

        if not subscriber_topic.endswith("#"):
            subscriber_topic = subscriber_topic + "#"
        # topic to subsribe to (can be different from the publishing topic)
        self.subscriber_topic = subscriber_topic

        # set username and password
        self.client.username_pw_set(username=cr.username, password=cr.password)

        # handle SSL encryption if enabled in credential.py settings
        if cr.isSSLEnabled:
            self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                                tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            self.client.tls_insecure_set(False)

        # binding callback functions
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message

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

    # create function for callback
    def on_publish(self, cl, userdata, result):
        logging.info("(MQTT Publisher) data published " + str(userdata))

    # gets called whenever subscribed topic has a new message
    def on_message(self, client, userdata, msg):
        logging.info("(MQTT Subscriber) data received: {} -> {}".format(
            str(msg.topic), str(msg.payload.decode())))
        # command should come from the message payload
        command = str(msg.payload.decode())
        # Name of the device contains in the topic, only the name direct under the top subscriber topic will be
        # used, anything after that will be discarde. For example:
        # if the top level subscriber topic is /devices/# and the incomming message has a topic of /devices/some_device/something_else/...
        # only the text "some_device" will be used as the direct device name
        if len(str(msg.topic)) > 0:
            device_name = str(msg.topic).split(
                self.subscriber_topic[:-1])[1].split("/")[0]
        if len(device_name) > 0 and len(command) > 0 and "RESPONSE" not in command.upper():
            # give current status of deivce
            if command.upper() == "STATUS":
                status = control.get_hue_http_device_status(device_name)
                self.client.publish(
                    msg.topic, "Response: {}:{}".format(device_name, status))
            # toggle device
            elif command.upper() in ["ON", "OFF"]:
                control.toggle_device(device_name, command)
            # in case not command supported
            else:
                logging.warning("(MQTT Subscriber) command {} not supported".format(
                    str(msg.payload.decode())))
                self.client.publish(
                    msg.topic, "Response: WARNING command \"{}\" is not supported".format(
                        str(msg.payload.decode())))

    def on_connect(self, cl, userdata, flags, rc):
        if rc == 0:
            logging.info("(MQTT) Successfully connected")
            self.client.isConnected = True

            # Subscribing in on_connect() means that if we lose the
            # connection and reconnect then subscriptions will be renewed.
            self.client.subscribe(self.subscriber_topic)
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
    mqtt = MQTTDataHelper(subscriber_topic="/test/")
    mqtt.publish_data_to_cloud("Hello World", "test")

    # time.sleep(5)
    # mqtt.publish_data_to_cloud("Hello World", "test")

    # time.sleep(5)
    # mqtt.publish_data_to_cloud("Hello World", "test")

    input("")
