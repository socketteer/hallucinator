# view.py
#
# Class representing a 3D viewing window transformation
# Written by Kyle McDonell
#
# CS 251
# Spring 2016
from functools import reduce

import numpy as np
import math

class View(object):

    # Initial viewing parameters
    def __init__(self):
        self.vrp = np.array([0.5, 0.5, 1], dtype=float)
        self.vpn = np.array([0, 0, -1], dtype=float)
        self.vup = np.array([0, 1, 0], dtype=float)
        self.u = np.array([-1, 0, 0], dtype=float)
        self.extent = np.array([1, 1, 1], dtype=float)
        self.screen = np.array([500, 500], dtype=float)
        self.offset = np.array([300, 100], dtype=float)

    # Resets the object to its default state
    def reset(self):
        self.__init__()

    # Creates a deep copy of the view object
    def clone(self):
        view = View()
        view.vrp = np.copy(self.vrp)
        view.vpn = np.copy(self.vpn)
        view.vup = np.copy(self.vup)
        view.u = np.copy(self.u)
        view.extent = np.copy(self.extent)
        view.screen = np.copy(self.screen)
        view.offset = np.copy(self.offset)
        return view

    # Build the np array representing the viewing transformation
    def build(self):
        # Build orthonormal basis
        tu = normalize(np.cross(self.vup, self.vpn))
        tvup = normalize(np.cross(self.vpn, tu))
        tvpn = normalize(np.copy(self.vpn))
        self.u = tu
        self.vup = tvup
        self.vpn = tvpn

        # Translate the view matrix
        t1 = get_translation_matrix(-self.vrp[0],
                                    -self.vrp[1],
                                    -self.vrp[2])

        # Rotate the view matrix
        r1 = get_rotation_matrix(tu, tvup, tvpn)

        # Translate the view matrix so the lower left corner
        # of the view space is at the origin
        t2 = get_translation_matrix(0.5 * self.extent[0],
                                    0.5 * self.extent[1],
                                    0)

        # Scale the view matrix to the screen
        s1 = get_scale_matrix(-self.screen[0] / self.extent[0],
                              -self.screen[1] / self.extent[1],
                              1.0 / self.extent[2])

        # Translate the view matrix so the lower left corner
        # is at the origin plus the view offset
        t3 = get_translation_matrix(self.screen[0] + self.offset[0],
                                    self.screen[1] + self.offset[1],
                                    0)

        # Get the viewing pipeline matrix
        vtm = np.identity(4, float)
        vtm = reduce(np.dot, [t3, s1, t2, r1, t1, vtm])
        return vtm


    # Rotate with respect to the origin
    def rotateOrigin(self, uAngle, vupAngle):
        # Axis align
        r1 = get_rotation_matrix(self.u, self.vup, self.vpn).T
        # Rotate U and VUP
        r2 = y_rot(vupAngle)
        r3 = x_rot(uAngle)
        # Get the rotation matrix and apply it to the axes
        rotate = reduce(np.dot, [r1.T, r3, r2, r1])
        self.vrp = np.dot(rotate, np.append(self.vrp, [1]))[:3]
        self.u = normalize(np.dot(rotate, np.append(self.u, [0]))[:3])
        self.vup = normalize(np.dot(rotate, np.append(self.vup, [0]))[:3])
        self.vpn = normalize(np.dot(rotate, np.append(self.vpn, [0]))[:3])

    # Rotate with respect to the VRC
    def rotateVRC(self, uAngle, vupAngle):
        # Translate to origin
        vrc = self.vrp + self.vpn * 0.5 * self.extent[2]
        t1 = get_translation_matrix(-vrc[0], -vrc[1], -vrc[2])
        # Axis align
        r1 = get_rotation_matrix(self.u, self.vup, self.vpn).T
        # Rotate U and VUP
        r2 = y_rot(vupAngle)
        r3 = x_rot(uAngle)
        # Translate back
        t2 = get_translation_matrix(vrc[0], vrc[1], vrc[2])

        # Get the rotation matrix and apply it to the axes
        rotate = reduce(np.dot, [t2, r1.T, r3, r2, r1, t1])
        self.vrp = np.array(np.dot(rotate, np.append(self.vrp, [1])))[:3]
        self.u = normalize(np.array(np.dot(rotate, np.append(self.u, [0])))[:3])
        self.vup = normalize(np.array(np.dot(rotate, np.append(self.vup, [0])))[:3])
        self.vpn = normalize(np.array(np.dot(rotate, np.append(self.vpn, [0])))[:3])




# Normalize the first three coordinates of a vector, ignoring its homogeneous coordinate
def normalize(vector, dim=None):
    if dim is None:
        dim = vector.size
    length = np.sqrt(np.sum(vector[:dim] * vector[:dim]))

    np.divide.at(vector, [i for i in range(dim)], length)
    return vector


# Np array to translate by the provided values
def get_translation_matrix(tx, ty, tz):
    return np.array([[1, 0, 0, tx],
                      [0, 1, 0, ty],
                      [0, 0, 1, tz],
                      [0, 0, 0, 1]], dtype=float)

# Np array to scale a vector by the provided coefficients
def get_scale_matrix(dx, dy, dz):
    return np.array([[dx, 0, 0, 0],
                      [0, dy, 0, 0],
                      [0, 0, dz, 0],
                      [0, 0, 0, 1]], dtype=float)

# Np array to rotate to align with the given orthonormal basis
def get_rotation_matrix(u, vup, vpn):
    return np.array([[u[0], u[1], u[2], 0],
                      [vup[0], vup[1], vup[2], 0],
                      [vpn[0], vpn[1], vpn[2], 0],
                      [0, 0, 0, 1]], dtype=float)

# Np array to rotate around the x axis by the given angle
def x_rot(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[1, 0, 0, 0],
                      [0, c, -s, 0],
                      [0, s, c, 0],
                      [0, 0, 0, 1]], dtype=float)

# Np array to rotate around the y axis by the given angle
def y_rot(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, 0, s, 0],
                      [0, 1, 0, 0],
                      [-s, 0, c, 0],
                      [0, 0, 0, 1]], dtype=float)


# Test
if __name__ == '__main__':
    v = View()
    print(v.build())
    print(np.dot(v.build(), np.array([0,0,0,1], dtype=float).T))
