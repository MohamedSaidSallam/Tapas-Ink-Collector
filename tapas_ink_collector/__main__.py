import datetime
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


def pullForPixelKey(locationKey, colorKey, **kargs):
    pullForPixel(*config["locations"][locationKey],
                 config["colors"][colorKey], **kargs)


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


def launchSequence():
    print('launching app')
    device.shell(
        f'monkey -p {config["appName"]} -c android.intent.category.LAUNCHER 1')

    print('waiting for splash screen')
    pullForPixelKey("menuButton",
                    "menuButtonBackground")

    tapLocaltion("menuButton")

    tapLocaltion("freeInk")


launchSequence()

timesDone = 0
startHour = datetime.datetime.now().hour
resetPeriod = 60 * 60  # one hour
maxTimes = 30

while True:
    print('waiting for watch video')
    pullForPixelKey('watchVideoButton',
                    "watchVideoButtonBackground")

    tapLocaltion('watchVideoButton')

    time.sleep(2.5)
    if isColorEqual(getPixel(*config["locations"]['watchVideoButton']), config["colors"]["background"]):
        print('waiting for no offers')
        pullForPixelKey('watchVideoButton',
                        "watchVideoButtonBackground", sleepAmount=1)

        tapLocaltion('watchVideoButton')

    print('waiting for ad to end')

    time.sleep(config["adSleepAmount"])
    device.shell(f'input keyevent 4')  # go back
    tapLocaltion('adClose')  # close ad

    print('waiting for ad to end: Done')

    print('waiting to claim ink')
    pullForPixelKey("claimInk",
                    "claimInkBackground")

    tapLocaltion("claimInk")

    timesDone += 1
    print(timesDone)
    print(timesDone == maxTimes, startHour != datetime.datetime.now().hour)
    if timesDone == maxTimes or startHour != datetime.datetime.now().hour:
        startHour = datetime.datetime.now().hour
        timesDone = 0
        launchSequence()
