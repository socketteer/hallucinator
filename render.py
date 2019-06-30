import numpy as np
import scipy.misc as smp
from array2gif import write_gif

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


def save_img(data, filename):
    smp.imsave('./images/{0}'.format(filename), data)



#todo fix to work with any color
def binary_to_bichrom(arr, foreground=WHITE, background=BLACK):
    """

    :param arr:
    :param foreground:
    :param background:
    :return:
    """

    bichrom = np.where(arr, 1, 0)
    return bichrom


def set_to_bichrome(points, x_range, y_range, foreground=WHITE, background=BLACK, canv="new"):
    """

    :param points:
    :param x_range:
    :param y_range:
    :param foreground:
    :param background:
    :param canv:
    :return:
    """
    if canv == "new":
        canv = np.full((x_range[1] - x_range[0], y_range[1] - y_range[0], 3), background, dtype=np.uint8)
    for p in points:
        if x_range[0] <= p[0] < x_range[1] and y_range[0] <= p[1] < y_range[1]:
            canv[p[0] - x_range[0], p[1] - y_range[0]] = foreground
    return canv


def project(points, pov=(0, 0, 0), z_scale=0.005, method='weak'):
    """
    :param points:
    :param pov:
    :param z_scale:
    :param method:
    :return:
    projects a three dimensional set of points onto a two dimensional
    canvas depicting a view from a point located at [pov]
    pointing in the positive z direction"""
    #check dims of array
    #check pov
    if method == "weak":
        new_points = set()
        for point in points:
            #print(point)
            if point[2] > 0:
                new_points.add((np.rint((point[0] - pov[0])/((point[2] - pov[2])*z_scale)).astype(int),
                                np.rint((point[1] - pov[1])/((point[2] - pov[2])*z_scale)).astype(int)))
        return new_points
    else:
        print('not implemented')


def animate(spacetime, step=1, fps=5, timedim=0):
    """
    :param spacetime: n+1-dimensional array of frames of n-dimensional space
    :param step: only where frame num % step == 0 will be included in animation
    :param fps: frames per second
    :param timedim: index for dimension of points representing time
    :return: gif
    """
    write_gif(spacetime, 'images/spacetime.gif', fps=fps)

dataset = [
    np.array([
        [[255, 0, 0], [255, 0, 0]],  # red intensities
        [[0, 255, 0], [0, 255, 0]],  # green intensities
        [[0, 0, 255], [0, 0, 255]]   # blue intensities
    ]),
    np.array([
        [[0, 0, 255], [0, 0, 255]],
        [[0, 255, 0], [0, 255, 0]],
        [[255, 0, 0], [255, 0, 0]]
    ])
]
