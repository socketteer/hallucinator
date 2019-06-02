import numpy as np
import scipy.misc as smp

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]

#TODO 3d


def canvas(w, h, color=BLACK):
    canvas = np.full( (w, h, 3), color, dtype=np.uint8)
    return canvas


def render_from_array(data):
    img = smp.toimage(data)
    img.show()


#todo fix to work with any color
def binary_to_bichrom(arr, foreground=WHITE, background=BLACK):
    bichrom = np.where(arr, 1, 0)
    return bichrom


'''parametric to bichrome'''


def set_to_bichrome(set, x_min, x_max, y_min, y_max, foreground=WHITE, background=BLACK):
    canvas = np.full((x_max - x_min, y_max - y_min, 3), background, dtype=np.uint8)
    for p in set:
        if x_min <= p[0] < x_max and y_min <= p[1] < y_max:
            canvas[p[0] - x_min, p[1] - y_min] = foreground
    return canvas
