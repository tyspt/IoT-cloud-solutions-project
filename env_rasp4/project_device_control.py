import json
import requests
import logging

import credential as cr

""" Module respobsible for controlling the offline devices connected to Raspberry Pi or Arduino with 
    either REST Http requests through LAN or messages through serial connection.
"""

# There are two way to control local devices in my project, using Http requests for the ones that are connected on my
# phillips hue bridge, or direct through raspberrry which are connected to a relay.
# Refer to the following page for more information about phillips hue bridge commands: https://developers.meethue.com/develop/get-started-2/

HUE_BRIDGE_HTTP_DEVICES = {"grow_light": "http://philips-hue/api/{}/lights/5/".format(cr.hue_bridge_api_key),
                           "water_heater": "http://philips-hue/api/{}/lights/3/".format(cr.hue_bridge_api_key)}
RELAY_DEVICES = [""]


def get_hue_http_device_status(device_name):
    endpoint = HUE_BRIDGE_HTTP_DEVICES[device_name]
    # sending get request and saving the response as response object
    r = requests.get(url=endpoint)
    # extracting data in json format
    response = r.json()
    # extracting data
    status = response["state"]["on"]
    if status is True:
        return "on"
    else:
        return "off"
    

def toggle_device(device_name, command):
    logging.info("(Device Control) device controlling info received, device: {} -> command: {}".format(device_name,
                                                                                                       command))
    if device_name in HUE_BRIDGE_HTTP_DEVICES.keys():
        _toggle_device_through_http_request(device_name, command)
    elif device_name in RELAY_DEVICES.keys():
        pass
    else:
        logging.warning(
            "(Device Control) unable to control device {}, because it doesn't exist in global configs".format(device_name))
        raise NotImplementedError

def _toggle_device_through_http_request(device_name, command):
    endpoint = HUE_BRIDGE_HTTP_DEVICES[device_name] + "state"

    data = None
    if command.upper() == "ON":
        data = json.dumps({"on": True})
    else:
        data = json.dumps({"on": False})

    # sending put request and saving response as response object
    r = requests.put(url=endpoint, data=data)
    
    # extracting response text
    pastebin_url = r.text

    logging.info("(Device Control) device {} is turned {}, message: {}".format(
        device_name, command, pastebin_url))
    
if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
                         level=logging.DEBUG)
    toggle_device("grow_light", "off")
