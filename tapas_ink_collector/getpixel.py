import io

import numpy
from PIL import Image


def getPixel(device, x, y):
    image = device.screencap()

    image = Image.open(io.BytesIO(image))
    image = numpy.array(image, dtype=numpy.uint8)

    return image[y][x]
