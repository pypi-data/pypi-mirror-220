import io

import cv2
import numpy as np

from chromahacker.spline import spline_from # hey this line is a palindrome
from chromahacker.process_image import url_to_image

def palettize(url, output, *args, accurate=False):
    np_array = url_to_image(url)

    img = cv2.cvtColor(np_array, cv2.COLOR_RGB2GRAY)

    fn = spline_from(*args)

    display = np.rint(fn(img)).astype(np.uint8)
    if accurate:
        display = np.array([[fn(j) for j in i] for i in img])
    else:
        display = fn(display)
    cv2.imwrite('wallpaper.' + output, display)
