import datetime
import sys
import time

from ppadb.client import Client as AdbClient

from tapas_ink_collector.config_loader import config
from tapas_ink_collector.getpixel import getPixel


def isColorEqual(color1, color2):
    return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]


def tap(location):
    device.shell(f'input tap {location[0]} {location[1]}')


def tapLocaltion(key):
    print(f'tapping {key}')
    tap(config["locations"][key])


adb = AdbClient(host=config["adb"]["host"], port=config["adb"]["port"])

devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()

device = devices[0]


def launchSequence():
    print('launching app')
    device.shell(
        f'monkey -p {config["appName"]} -c android.intent.category.LAUNCHER 1')

    # wait for splash screen to appear in case the app was already open
    # since it see the previous bottom nav as if it's
    time.sleep(1)
    print('waiting for splash screen')
    pullForPixelKey("menuButton",
                    "menuButtonBackground")

    time.sleep(1)
    tapLocaltion("menuButton")

    tapLocaltion("freeInk")


def pullForPixel(x, y, color, sleepAmount=0.5, timeoutCallBack=launchSequence):
    count = 0
    while True:
        pixel = getPixel(device, x, y)

        print(
            f'pulling pixel, Count: {count}, Pixel: {pixel}, Target: {color}')

        if isColorEqual(pixel, color):
            break

        count += 1
        if count == 100:
            timeoutCallBack()
            break
        time.sleep(sleepAmount)


def pullForPixelKey(locationKey, colorKey, **kargs):
    pullForPixel(*config["locations"][locationKey],
                 config["colors"][colorKey], **kargs)


launchSequence()

timesDone = 0
startHour = datetime.datetime.now().hour
maxTimes = config["maxTimes"]


def reset(newStartHour):
    global timesDone, startHour
    startHour = newStartHour
    timesDone = 0
    launchSequence()


while True:
    ###################### Tap Watch Video ######################
    print('waiting for watch video')
    pullForPixelKey('watchVideoButton',
                    "watchVideoButtonBackground")

    tapLocaltion('watchVideoButton')

    time.sleep(0.5)
    buttonColor = getPixel(device, *config["locations"]['watchVideoButton'])

    if isColorEqual(buttonColor, config["colors"]["watchVideoButtonBackground"]):
        print('button still there, tapping again')
        tapLocaltion('watchVideoButton')
    elif isColorEqual(buttonColor, config["colors"]["background"]):
        print('waiting for no offers')
        pullForPixelKey('watchVideoButton',
                        "watchVideoButtonBackground", sleepAmount=1)

        tapLocaltion('watchVideoButton')
    ###################### Tap Watch Video END ######################

    ###################### AD Part ######################
    print('waiting for ad to end')

    time.sleep(config["adSleepAmount"])

    if isColorEqual(
        getPixel(
            device,
            *config["locations"]['watchVideoButton']),
        config["colors"]["watchVideoButtonBackground"]
    ):
        print('the ad was a lie')
        continue

    device.shell('input keyevent 4')  # go back
    tapLocaltion('adClose')

    print('waiting for ad to end: Done')
    ###################### AD Part: END ######################

    ###################### Claim Reward ######################
    print('waiting to claim ink')
    pullForPixelKey("claimInk",
                    "claimInkBackground")

    tapLocaltion("claimInk")
    ###################### Claim Reward: END ######################

    timesDone += 1
    print('timesDone', timesDone)

    currentTime = datetime.datetime.now()
    print('Restart Conditions: ')
    print('startHour != currentTime.hour', startHour != currentTime.hour)
    print('timesDone == maxTimes', timesDone == maxTimes)

    if startHour != currentTime.hour:
        print('An hour passed, Restarting')
        reset(currentTime.hour)
    elif timesDone == maxTimes:
        nextHour = datetime.datetime(
            currentTime.year,
            currentTime.month,
            currentTime.day + ((startHour+1) // 24),
            (startHour+1) % 24
        )
        sleepTime = (nextHour - currentTime).total_seconds()
        print(f'Sleeping for {sleepTime}s')
        time.sleep(sleepTime)

        reset(datetime.datetime.now().hour)
