import math
import ikonal
import numpy as np

IDENTITY3 = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

IDENTITY4 = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])


def transform(transformation, obj):
    new = obj
    new.position = np.matmul(new.position, transformation)
    return new


'''transformation matrices'''


# TODO shear

def translate(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])


def rotate(theta):
    return np.array([[math.cos(theta), -math.sin(theta), 0],
                     [math.sin(theta), math.cos(theta), 0],
                     [0, 0, 1]])


def scale(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])


def rotate_about(theta, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), rotate(theta)), translate(-p[0], -p[1]))


def scale_about(sx, sy, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), scale(sx, sy)), translate(-p[0], -p[1]))


'''3d transforms'''


def rotate_3(theta, axis='X'):
    pass


def rotate_about_3(theta, axis='X'):
    pass


def translate_3(tx, ty, tz):
    pass


def scale_3(sx, sy, sz):
    pass


def scale_about_3(sx, sy, sz, p=(0, 0, 0)):
    pass


def weak_project(pov=(0, 0, 0), z_scale=0.005):
    """
    :param pov:
    :param z_scale:
    :return:
    returns an operator which projects a three dimensional
    set of points onto a two dimensional
    canvas depicting a view from a point located at [pov]
    pointing in the positive z direction"""

    return lambda xyz: ((xyz[0] - pov[0]) / ((xyz[2] - pov[2]) * z_scale),
                        (xyz[1] - pov[1]) / ((xyz[2] - pov[2]) * z_scale))
