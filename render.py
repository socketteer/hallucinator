import numpy as np
import scipy.misc as smp

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#TODO 3d


def canvas(w, h, color=BLACK):
    canv = np.full( (w, h, 3), color, dtype=np.uint8)
    return canv


def render_from_array(data):
    img = smp.toimage(np.rot90(data))
    img.show()


#todo fix to work with any color
def binary_to_bichrom(arr, foreground=WHITE, background=BLACK):
    bichrom = np.where(arr, 1, 0)
    return bichrom


'''parametric to bichrome'''


def set_to_bichrome(points, x_range, y_range, foreground=WHITE, background=BLACK):
    canv = np.full((x_range[1] - x_range[0], y_range[1] - y_range[0], 3), background, dtype=np.uint8)
    for p in points:
        if x_range[0] <= p[0] < x_range[1] and y_range[0] <= p[1] < y_range[1]:
            canv[p[0] - x_range[0], p[1] - y_range[0]] = foreground
    return canv
