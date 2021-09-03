import os

import numpy
from PIL import Image

from tapas_ink_collector.config_loader import config

os.makedirs(config["outputFolder"], exist_ok=True)
TEMP_IMG_PATH = f'{config["outputFolder"]}/screen.png'


def getPixel(device, x, y):
    image = device.screencap()

    with open(TEMP_IMG_PATH, 'wb') as f:
        f.write(image)

    image = Image.open(TEMP_IMG_PATH)
    image = numpy.array(image, dtype=numpy.uint8)

    return image[y][x]