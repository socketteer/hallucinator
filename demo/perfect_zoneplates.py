import sys

sys.path.append('../hallucinator')

import math
import hallucinator as hl
import numpy as np


def squarewave(x):
    return 0 if x - math.floor(x) < 0.5 else 1


def sinwave(x):
    return math.sin(x * 2 * math.pi)


def ripple(x, y, wavelength):
    return squarewave(math.sqrt(x ** 2 + y ** 2) / wavelength ** 2)


def zoneplate(x, y, wavelength, exp):
    return squarewave(math.sqrt(x ** 2 + y ** 2) ** exp / wavelength ** 2)


def sample(function, a_range, b_range, a_density, b_density):
    a_length = a_range[1] - a_range[0]
    b_length = b_range[1] - b_range[0]
    points = set()
    for a in np.linspace(a_range[0], a_range[1], a_length * a_density):
        for b in np.linspace(b_range[0], b_range[1], b_length * b_density):
            points.add((a, b, function(a, b)))

    return points


def sample_log(function, a_range, b_range, a_density, b_density):
    a_length = a_range[1] - a_range[0]
    b_length = b_range[1] - b_range[0]
    points = set()
    for a in np.geomspace(a_range[0], a_range[1], num=a_length * a_density):
        for b in np.geomspace(b_range[0], b_range[1], num=b_length * b_density):
            # print(a, b)
            points.add((a, b, function(a, b)))

    return points


def make_ripple(x_range, y_range, x_density, y_density, wavelength):
    pts = sample(lambda a, b: ripple(a, b, wavelength), x_range, y_range, x_density, y_density)
    canv = hl.set_to_gradient(pts,
                              x_range=x_range,
                              y_range=y_range,
                              black_ref=-1,
                              white_ref=1,
                              default=hl.GRAY,
                              resolution=50)
    return canv


def make_zoneplate(x_range, y_range, x_density, y_density, wavelength, resolution, exp):
    pts = sample(lambda a, b: zoneplate(a, b, wavelength, exp), x_range, y_range, x_density, y_density)
    canv = hl.set_to_gradient(pts,
                              x_range=x_range,
                              y_range=y_range,
                              black_ref=-1,
                              white_ref=1,
                              default=hl.GRAY,
                              resolution=resolution)
    return canv


x_range = (-20, 20)
y_range = (-20, 20)
x_density = 10
y_density = 10
wavelength = 1
resolution = 30
exp = 2.5

canv = make_zoneplate(x_range, y_range, x_density, y_density, wavelength, resolution, exp)
hl.render_from_array(canv)
hl.save_img(canv, 'zoneplates/discrete-zoneplate_xd{2}-yd{3}-w{4}-r{5}-exp{6}'.format(x_range,
                                                                                      y_range,
                                                                                      x_density,
                                                                                      y_density,
                                                                                      wavelength,
                                                                                      resolution,
                                                                                      exp))

'''hl.video(frame_func=lambda t: make_zoneplate(x_range=x_range,
                                             y_range=y_range,
                                             x_density=x_density,
                                             y_density=y_density,
                                             wavelength=0.1 / (t / 2 + 1)),
         filename='zoneplates/zoneplates_change_wavelength_3',
         t_range=(0, 15),
         FPS=10)'''
