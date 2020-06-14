import copy
from enum import Enum

import numpy as np
import numexpr as ne
import math
import hallucinator as hl


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
    return np.linalg.norm(p1-p2)


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
#################################################################


# Takes a plane of x-y coordinates at z=0 and returns an array of path-lengths from the point p
# shape (n, m, 2) -> (n, m)
def perspective_plane(xy, p=(0, 0, 10)):
    pxy = p[:-1]
    x2y2 = ne.evaluate("sum((xy-pxy)**2, axis=2)")
    z2 = p[-1]**2
    return ne.evaluate("sqrt(x2y2+z2)")


# Is this right?
def fourier_plane(xy, p=(0, 0)):
    return perspective_plane(xy, p=(*p[:2], 0))


# Turns a perspective plane into a zone plate with the given wavelength
# shape (n, m) -> (n, m)
def perspective_zp(persp_plane, wavelength=0.01):
    frequency = 2 * math.pi / wavelength
    return ne.evaluate("sin(persp_plane*frequency)")


def opl_zp(persp_plane, wavelength=0.01):
    frequency = 2 * math.pi / wavelength
    return ne.evaluate("persp_plane*frequency")


def phase_threshold(values, threshold=2*math.pi):
    return ne.evaluate("values % threshold")


def real(values):
    return ne.evaluate("cos(values)")


def imaginary(values):
    return ne.evaluate("sin(values)")


def phase_conjugate(values, threshold=2*math.pi):
    return ne.evaluate("threshold - values")


'''xy = xy_plane()
persp_xy = perspective_plane(xy)
zp = perspective_zp(persp_xy)
hl.render_from_array(imagify(xy))
hl.render_from_array(imagify(persp_xy))
hl.render_from_array(imagify(zp))'''

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





##################################################################
# This is too cute. They need to collapse into numpy arrays too quickly.
##################################################################

# class Zoneplate:
#
#     class types(Enum):
#         FRESNEL = "Fresnel"
#         FOURIER = "Fourier"
#         LINEAR = "Linear"
#         EXPONENTIAL = "Exponential"
#         CUSTOM = "Custom"
#
#     def __init__(self,
#                  type=types.FRESNEL,
#                  wavelength=0.01,
#                  center=(0, 0, 10),
#                  value_range=(-1, 1),
#                  resolution=(-1, 1)
#                  ):
#
#         self.type = type
#         self.wavelength = wavelength
#         self.center = center
#         self.value_range = value_range
#         self.resolution = resolution
#         self._evaluated = None
#
#     def evaluate_fresnel(self):
#         xy = hl.xy_plane(value_range=self.value_range, resolution=self.resolution)
#         persp_plane = hl.perspective_plane(p=self.center, xy=xy)
#         return hl.phase_threshold(hl.opl_zp(persp_plane, wavelength=self.wavelength))
#
#     def evaluate(self):
#         if self.type == Zoneplate.types.FRESNEL:
#             return self.evaluate_fresnel()
#         else:
#             raise NotImplementedError(f"{self.type} zone plate not implemented")
#
#     # Lazy property, evaluate the zoneplate on a plane
#     @property
#     def evaluated(self):
#         if self._evaluated is None:
#             self._evaluated = self.evaluate()
#         return self._evaluated
#
#     def __add__(self, other):
#         if isinstance(other, Zoneplate):
#             other = other.evaluated
#         return hl.phase_threshold(self.evaluated + other)
#
#     def __radd__(self, other):
#         if isinstance(other, Zoneplate):
#             other = other.evaluated
#         return hl.phase_threshold(self.evaluated + other)
#
#     def __sub__(self, other):
#         print(type(other.evaluated), type(self.evaluated))
#         return hl.phase_threshold(self.evaluated - other.evaluated)
#
#     def __rsub__(self, other):
#         if isinstance(other, Zoneplate):
#             other = other.evaluated
#         return hl.phase_threshold(self.evaluated - other)
#
#     def __invert__(self):
#         new = copy.copy()
#         new.type = self.type
#         new._evaluated = hl.phase_conjugate(self.evaluated)
#         return new
#
#     def __repr__(self):
#         return f"Zp( type={self.type}"


