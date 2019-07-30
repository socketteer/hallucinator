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

ORTHO_PROJECT = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 1]])


def weak_project(z_factor=0.02):
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, z_factor, 0]])


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


# TODO make general
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


'''2d chained transforms'''


def shear_about(sx=0, sy=0, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), shear(sx, sy)), translate(-p[0], -p[1]))


def mirror_about(axis='x', offset=0):
    if axis == 'x':
        return np.matmul(np.matmul(translate(tx=offset), mirror(axis)), translate(tx=-offset))


def rotate_about(theta, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), rotate(theta)), translate(-p[0], -p[1]))


def scale_about(sx, sy, p=(0, 0)):
    return np.matmul(np.matmul(translate(p[0], p[1]), scale(sx, sy)), translate(-p[0], -p[1]))


'''3d transforms'''


# TODO mirroring


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


def shear_3(xy=0, xz=0, yx=0, yz=0, zx=0, zy=0):
    return np.array([[1, xy, xz, 0],
                     [yx, 1, yz, 0],
                     [zx, zy, 1, 0],
                     [0, 0, 0, 1]])


'''3d chained transformations'''


def rotate_about_3(theta, axis=(1, 0, 0), p=(0, 0, 0)):
    if p == (0, 0, 0):
        return rotate_3(theta, axis)
    else:
        return np.matmul(np.matmul(translate_3(p[0], p[1], p[2]),
                                   rotate_3(theta, axis)),
                         translate_3(-p[0], -p[1], -p[2]))


def scale_about_3(sx, sy, sz, p=(0, 0, 0)):
    if p == (0, 0, 0):
        return scale_3(sx, sy, sz)
    else:
        return np.matmul(np.matmul(translate_3(p[0], p[1], p[2]),
                                   scale_3(sx, sy, sz)),
                         translate_3(-p[0], -p[1], -p[2]))


def shear_about_3(xy=0, xz=0, yx=0, yz=0, zx=0, zy=0, p=(0, 0, 0)):
    if p == (0, 0, 0):
        return shear_3(xy, xz, yx, yz, zx, zy)
    else:
        return np.matmul(np.matmul(translate_3(p[0], p[1], p[2]),
                                   shear_3(xy, xz, yx, yz, zx, zy)),
                         translate_3(-p[0], -p[1], -p[2]))
