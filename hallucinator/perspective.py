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


def parabola(p):
    return 0.1*(p[0]**2 + p[1]**2)


def slope(p):
    return p[0]


def sloped_parabola(p):
    return slope(p) + parabola(p)


def perspective_transform(coordinates, wavelength, f, surface=lambda p: 0):
    def perspective(p):
        distance = dist(coordinates, np.array([*p, surface(p)]))
        phase_change = phase(distance, wavelength)
        return math.sin(f(p) + phase_change)
    return perspective


def depth_map(wavelength, surface=lambda p: 0):
    def depth(p):
        distance = surface(p)
        return math.sin(phase(distance, wavelength))

    return depth


'''plane = hl.sampling_image(f, value_range=(-10, 10), image_size=(1000, 1000), binary=False)
hl.render_from_array(plane)'''

zp = perspective_transform(np.array([0, 0, 10]), 0.01, lambda p: 1)
plane = hl.sampling_image(zp, value_range=(-10, 10), image_size=(500, 500), binary=False)
hl.render_from_array(plane)

'''par = depth_map(wavelength=1, surface=sloped_parabola)
plane = hl.sampling_image(par, value_range=(-10, 10), image_size=(1500, 1500),
                          binary=True, parallel_sample=True)
hl.render_from_array(plane)'''

persp = perspective_transform(np.array([0, 0, 10]), 0.01, zp)
plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=True)
print(np.sum(plane2/127.5-1))
hl.render_from_array(plane2)


persp = perspective_transform(np.array([1, 0, 10]), 0.01, zp)
plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=True)
print(np.sum(plane2/127.5-1))
hl.render_from_array(plane2)

persp = perspective_transform(np.array([10, 0, 10]), 0.01, zp)
plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=True)
print(np.sum(plane2/127.5-1))
hl.render_from_array(plane2)

persp = perspective_transform(np.array([0, 0, 15]), 0.01, zp)
plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=True)
print(np.sum(plane2/127.5-1))
hl.render_from_array(plane2)

persp = perspective_transform(np.array([1, 0, 15]), 0.01, zp)
plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=True)
print(np.sum(plane2/127.5-1))
hl.render_from_array(plane2)

persp = perspective_transform(np.array([10, 0, 15]), 0.01, zp)
plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=True)
print(np.sum(plane2/127.5-1))
hl.render_from_array(plane2)