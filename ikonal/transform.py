import math
import numpy as np

IDENTITY3 = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

IDENTITY4 = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

'''transformation matrices'''

# TODO gen
ORTHO_PROJECT = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 1]])


# TODO mirror arbitrary axis

def translate(tx=0, ty=0):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])


def rotate(theta):
    return np.array([[math.cos(theta), -math.sin(theta), 0],
                     [math.sin(theta), math.cos(theta), 0],
                     [0, 0, 1]])


def scale(sx=1, sy=1):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])


def shear(sx=0, sy=0):
    return np.array([[1, sx, 0],
                     [sy, 1, 0],
                     [0, 0, 1]])


def mirror(axis='x'):
    if axis == 'x':
        return np.array([[-1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])
    elif axis == 'y':
        return np.array([[1, 0, 0],
                         [0, -1, 0],
                         [0, 0, 1]])
    else:
        print('mirror: invalid axis')


def shear_about(sx=0, sy=0, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), shear(sx, sy)), translate(-p[0], -p[1]))


# TODO more axes and general
def mirror_about(axis='x', offset=0):
    if axis == 'x':
        return np.matmul(np.matmul(translate(tx=offset), mirror(axis)), translate(tx=-offset))


def rotate_about(theta, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), rotate(theta)), translate(-p[0], -p[1]))


def scale_about(sx, sy, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), scale(sx, sy)), translate(-p[0], -p[1]))


'''3d transforms'''


# TODO shear, mirroring


def rotate_about_3(theta, axis=(1, 0, 0), p=(0, 0, 0)):
    if p == (0, 0, 0):
        return rotate_3(theta, axis)
    else:
        return np.matmul(np.matmul(translate_3(p[0], p[1], p[2]),
                                   rotate_3(theta, axis)),
                         translate_3(-p[0], -p[1], -p[2]))


def rotate_3(theta, axis=(1, 0, 0)):
    l, m, n = axis
    u = (1 - math.cos(theta))
    cos = math.cos(theta)
    sin = math.sin(theta)
    return np.array([[l * l * u + cos,
                      m * l * u - n * sin,
                      n * l * u + m * sin,
                      0],
                     [l * m * u + n * sin,
                      m * m * u + cos,
                      n * m * u - l * sin,
                      0],
                     [l * n * u - m * sin,
                      m * n * u + l * sin,
                      n * n * u + cos,
                      0],
                     [0,
                      0,
                      0,
                      1]])


def translate_3(tx, ty, tz):
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])


def scale_3(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def scale_about_3(sx, sy, sz, p=(0, 0, 0)):
    return np.matmul(np.matmul(translate_3(p[0], p[1], p[2]),
                               scale_3(sx, sy, sz)),
                     translate_3(-p[0], -p[1], -p[2]))
