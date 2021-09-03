import os
import time

import numpy
from PIL import Image
from ppadb.client import Client as AdbClient

from tapas_ink_collector.config_loader import config

os.makedirs(config["outputFolder"], exist_ok=True)
TEMP_IMG_PATH = f'{config["outputFolder"]}/screen.png'


def getPixel(x, y):
    image = device.screencap()

    with open(TEMP_IMG_PATH, 'wb') as f:
        f.write(image)

    image = Image.open(TEMP_IMG_PATH)
    image = numpy.array(image, dtype=numpy.uint8)

    return image[y][x]


def isColorEqual(color1, color2):
    return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]


def pullForPixel(x, y, color, sleepAmount=0.5):
    while True:
        pixel = getPixel(x, y)
        print(pixel)
        if isColorEqual(pixel, color):
            break
        time.sleep(sleepAmount)


def tap(location):
    device.shell(f'input tap {location[0]} {location[1]}')


def tapLocaltion(key):
    print(f'tapping {key}')
    tap(config["locations"][key])


adb = AdbClient(host=config["adb"]["host"], port=config["adb"]["port"])

devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]


print('launching app')
device.shell(
    f'monkey -p {config["appName"]} -c android.intent.category.LAUNCHER 1')

print('waiting for splash screen')
pullForPixel(*config["locations"]["menuButton"],
             config["colors"]["menuButtonBackground"])

tapLocaltion("menuButton")

tapLocaltion("freeInk")

while True:
    print('waiting for watch video')
    pullForPixel(*config["locations"]['watchVideoButton'],
                 config["colors"]["watchVideoButtonBackground"])

    tapLocaltion('watchVideoButton')

    time.sleep(2.5)
    if isColorEqual(getPixel(*config["locations"]['watchVideoButton']), config["colors"]["background"]):
        print('waiting for no offers')
        pullForPixel(*config["locations"]['watchVideoButton'],
                     config["colors"]["watchVideoButtonBackground"], sleepAmount=1)

        tapLocaltion('watchVideoButton')

    print('waiting for ad to end')

    time.sleep(config["adSleepAmount"])
    device.shell(f'input keyevent 4')  # go back
    tapLocaltion('adClose')  # close ad

    print('waiting for ad to end: Done')

    print('waiting to claim ink')
    pullForPixel(*config["locations"]["claimInk"],
                 config["colors"]["claimInkBackground"])

    tapLocaltion("claimInk")


# todo hourly limit
# todo hourly limit refersh stack view
