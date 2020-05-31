import numpy as np
import matplotlib.pyplot as plt
import hallucinator as hl
import math


def sample_plane(x_range, y_range, f):
    x_size = x_range[1] - x_range[0]
    y_size = y_range[1] - y_range[0]
    plane = np.empty([x_size, y_size])
    for a in range(x_size):
        for b in range(y_size):
            plane[a][b] = f(x_range[0]+a, y_range[0]+b)

    return plane


def f(p):
    return math.sin(p[0]**2 + p[1]**2)


def phase(distance, wavelength):
    return distance * 2 * math.pi / wavelength


def dist(p1, p2):
    return hl.pnorm(2)((p1-p2))


def perspective_transform(coordinates, wavelength, f):
    def perspective(p):
        distance = dist(coordinates, np.array([*p, 0]))
        phase_change = phase(distance, wavelength)
        return math.sin(f(p) + phase_change)
    return perspective



'''plane = hl.sampling_image(f, value_range=(-10, 10), image_size=(1000, 1000), binary=False)
hl.render_from_array(plane)'''

zp = perspective_transform(np.array([0, 0, 1]), 0.01, lambda p: 1)
plane = hl.sampling_image(zp, value_range=(-1, 1), image_size=(500, 500), binary=False)
hl.render_from_array(plane)

'''persp = perspective_transform(np.array([100, 0, 100]), 0.01, zp)
plane2 = hl.sampling_image(persp, value_range=(-10, 10), image_size=(1000, 1000))
hl.render_from_array(plane2)'''
