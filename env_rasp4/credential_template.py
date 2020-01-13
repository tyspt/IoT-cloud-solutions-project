
''' This is only a template configuration file for MQTT broker server, you need to fill in 
    your own login information, and change file name to "credential.py" in order to make it work.
'''
isSSLEnabled = False
broker = "your.broker.ip.address"
port = your.own.port
username = "your.username"
password = "your.password"

# this is used for controlling phillips hue devices, you can ignore it if you don't use a hue bridge to control your local devices
# Refer to the following page for more information: https://developers.meethue.com/develop/get-started-2/
hue_bridge_api_key = "api.key.for.phillips.hue.bridge"
