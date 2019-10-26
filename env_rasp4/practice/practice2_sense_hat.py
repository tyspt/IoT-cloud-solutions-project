from sense_hat import SenseHat
import time, random, requests

sense = SenseHat()
sense.clear()

blue = (0, 0, 255)
yellow = (255, 255, 0)

# sense.show_message("Test")

# sense.show_letter("Z", text_colour=yellow, back_colour=blue)

# while True:
#     sense.show_letter("3", text_colour=yellow, back_colour=blue)
#     time.sleep(1)

# print("Hellow World")

# Show Temperature, Pressure and Humidity
# sense.clear()
# while True:
#     pressure = sense.get_pressure()
#     temp = sense.get_temperature()
#     humidity = sense.get_humidity()

#     print(f"Pressure: {pressure}, Temperature: {temp}, Humidity: {humidity}")
#     time.sleep(1)


# Orientation
# red = (255, 0, 0)
# while True:
#     acceleration = sense.get_accelerometer_raw()
#     x = acceleration['x']
#     y = acceleration['y']
#     z = acceleration['z']
#     x = abs(x)
#     y = abs(y)
#     z = abs(z)

#     if x > 1 or y > 1 or z > 1:
#         sense.show_letter("!", red)
#     else:
#         sense.clear()



#Write informationn into the google sheet from last practice
while True:
    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humid = sense.get_humidity()

    res = requests.get(f"https://script.google.com/macros/s/AKfycbwL2WIo-pGNGoiX2EAwY7BXiwV04Re2lTS7jSRnDZEeW1hOx8w/exec?Temp={temp}&Humid={humid}")

    print(res)
    time.sleep(5)