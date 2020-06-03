import collections

import numpy as np
import numexpr as ne
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


##################################################################
# Kyle's new strange code
##################################################################

def xy_plane(value_range=(-1, 1), resolution=(1000, 1000), grid=True):
    resolution_x = resolution[0] if isinstance(resolution, collections.abc.Sequence) else resolution
    resolution_y = resolution[1] if isinstance(resolution, collections.abc.Sequence) else resolution
    value_range_x = value_range[0] if isinstance(value_range[0], collections.abc.Sequence) else value_range
    value_range_y = value_range[1] if isinstance(value_range[0], collections.abc.Sequence) else value_range

    x_axis = hl.np.linspace(start=value_range_x[0], stop=value_range_x[1], num=int(resolution_x))
    y_axis = hl.np.linspace(start=value_range_y[0], stop=value_range_y[1], num=int(resolution_y))
    # Perturb by 1/3 the step size if not a grid
    if not grid:
        x_offset = (x_axis[1] - x_axis[0])/3.0
        x_axis += np.random.uniform(low=-x_offset, high=x_offset, size=x_axis.shape)
        y_offset = (x_axis[1] - x_axis[0])/3.0
        y_axis += np.random.uniform(low=-y_offset, high=y_offset, size=x_axis.shape)

    # meshgrid returns [(x, y) for x in x_axis, y in y_axis]
    meshgrid = hl.np.meshgrid(x_axis, y_axis)
    xy = hl.np.stack(meshgrid, axis=2)
    # shape: (1000, 1000, 2)
    return xy


# Takes a plane of x-y coordinates at z=0 and returns an array of path-lengths from the point p
# shape (n, m, 2) -> (n, m)
def perspective_plane(xy, p=(0, 0, 10)):
    pxy = p[:-1]
    x2y2 = ne.evaluate("sum((xy-pxy)**2, axis=2)")
    z2 = p[-1]**2
    return ne.evaluate("sqrt(x2y2+z2)")


# Turns a perspective plane into a zone plate with the given wavelength
# shape (n, m) -> (n, m)
def perspective_zp(persp_plane, wavelength=0.01):
    period = 2 * math.pi / wavelength
    return ne.evaluate("sin(persp_plane*period)")


def imagify(arr):
    return np.interp(arr, (arr.min(), arr.max()), (0, 255)).astype(hl.np.uint8)


xy = xy_plane()
persp_xy = perspective_plane(xy)
zp = perspective_zp(persp_xy)
hl.render_from_array(imagify(xy))
hl.render_from_array(imagify(persp_xy))
hl.render_from_array(imagify(zp))

# hl.video2(
#     frame_function=lambda z: imagify(perspective_zp(x2y2, z)),
#     frame_arguments=np.geomspace(1, 1000, num=200),
#     fps=10,
#     preview=False,
#     filename="../images/perspective_zone"
# )


##################################################################
# Demos
##################################################################


#
# plane = hl.sampling_image(f, value_range=(-10, 10), image_size=(1000, 1000), binary=False)
# hl.render_from_array(plane)
#
# zp = perspective_transform(np.array([0, 0, 10]), 0.01, lambda p: 1)
# plane = hl.sampling_image(zp, value_range=(-10, 10), image_size=(500, 500), binary=False)
# hl.render_from_array(plane)
#
# par = depth_map(wavelength=1, surface=sloped_parabola)
# plane = hl.sampling_image(par, value_range=(-10, 10), image_size=(1500, 1500),
#                           binary=True, parallel_sample=True)
# hl.render_from_array(plane)
#
# persp = perspective_transform(np.array([0, 0, 10]), 0.01, zp)
# plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=False)
# print(np.sum(plane2/127.5-1))
# hl.render_from_array(plane2)
#
#
# persp = perspective_transform(np.array([1, 0, 10]), 0.01, zp)
# plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=False)
# print(np.sum(plane2/127.5-1))
# hl.render_from_array(plane2)
#
# persp = perspective_transform(np.array([10, 0, 10]), 0.01, zp)
# plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=False)
# print(np.sum(plane2/127.5-1))
# hl.render_from_array(plane2)
#
# persp = perspective_transform(np.array([0, 0, 15]), 0.01, zp)
# plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=False)
# print(np.sum(plane2/127.5-1))
# hl.render_from_array(plane2)
#
# persp = perspective_transform(np.array([1, 0, 15]), 0.01, zp)
# plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=False)
# print(np.sum(plane2/127.5-1))
# hl.render_from_array(plane2)
#
# persp = perspective_transform(np.array([10, 0, 15]), 0.01, zp)
# plane2 = hl.sampling_image(persp, value_range=(-3, 3), image_size=(1500, 1500), parallel_sample=False)
# print(np.sum(plane2/127.5-1))
# hl.render_from_array(plane2)
