import time

import numpy
from PIL import Image
from ppadb.client import Client as AdbClient


def getPixel(x, y):
    image = device.screencap()

    with open('output/screen.png', 'wb') as f:
        f.write(image)

    image = Image.open('output/screen.png')
    image = numpy.array(image, dtype=numpy.uint8)

    return image[y][x]


def isColorEqual(color1, color2):
    return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]


def pullForPixel(x, y, color, sleepAmount=0.5):
    pulling = True
    while pulling:
        time.sleep(sleepAmount)
        pixel = getPixel(x, y)
        print(pixel)
        pulling = not isColorEqual(pixel, color)


adb = AdbClient(host="127.0.0.1", port=5037)

devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]


print('launching app')
device.shell(f'monkey -p com.tapastic -c android.intent.category.LAUNCHER 1')

width, height = device.shell(f'wm size').split()[-1].split('x')

print('waiting for splash screen')
pullForPixel(int(width) - 1, int(height) - 1, [33, 33, 33])

print('hitting menu button')
device.shell(f'input tap {int(width) -1} {int(height) - 1}')

print('hitting free ink')
device.shell(f'input tap 150 640')

while True:
    print('waiting for watch video')
    pullForPixel(925, 1125, [238, 238, 238])

    print('hitting watch video')
    device.shell(f'input tap 937 1112')
    time.sleep(2.5)
    if isColorEqual(getPixel(302, 1096), [58, 58, 58]):
        print('waiting for no offers')
        pullForPixel(925, 1125, [238, 238, 238], sleepAmount=1)

        print('hitting watch video')
        device.shell(f'input tap 937 1112')


    print('waiting for ad to end')
    time.sleep(50)
    print(device.shell(f'input keyevent 4'))  # go back
    device.shell(f'input tap 1015 62')
    print('waiting for ad to end: Done')

    print('waiting to claim ink')
    pullForPixel(606, 1169, [160, 221, 175])

    print('claiming ink')
    device.shell(f'input tap 606 1169')


# todo hourly limit
# todo hourly limit refersh stack view
