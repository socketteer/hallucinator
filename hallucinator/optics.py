import itertools
import math
from pathos.multiprocessing import ProcessingPool as Pool

import hallucinator as hl
import numpy as np
import random

# TODO integrate
# TODO make 3d

C = 3 * 10 ** 8

"""color frequencies"""
RED_F = 430 * 10 ** 12
ORANGE_F = 480 * 10 ** 12
YELLOW_F = 510 * 10 ** 12
GREEN_F = 540 * 10 ** 12
CYAN_F = 580 * 10 ** 12
BLUE_F = 610 * 10 ** 12
VIOLET_F = 670 * 10 ** 12


def distance(p1, p2):
    return np.linalg.norm(p1 - p2)


def polar_to_cart(polar):
    x = polar[0] * np.cos(polar[1])
    y = polar[0] * np.sin(polar[1])
    return x, y


def cart_to_polar(cart):
    amplitude = np.sqrt(cart[0] ** 2 + cart[1] ** 2)
    phase = np.arctan2(cart[1], cart[0])
    return amplitude, phase


def real_field_at(sources, location):
    return field_at(sources, location)[0]


def field_at(sources, location):
    """returns field vector after interference of sources
    at location in cartesian coordinates"""
    vector = polar_to_cart(sources[0].detect(location))
    for source in sources[1:]:
        vector = np.add(vector, polar_to_cart(source.detect(location)))
    return vector


def intensity_at(sources, location):
    vector = field_at(sources, location)
    return vector[0] ** 2 + vector[1] ** 2


def eval_surface(sources, surface, a_range, b_range,
                        a_length='auto',
                        b_length='auto',
                        mode = 'grid',
                        func=intensity_at,
                        a_density=1,
                        b_density=1):
    points = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]

    a_coords = np.linspace(a_range[0], a_range[1], a_length * a_density)
    b_coords = np.linspace(b_range[0], b_range[1], b_length * b_density)
    eval_points = list(itertools.product(a_coords, b_coords))

    def eval_random_point(_):
        a = random.uniform(a_range[0], a_range[1])
        b = random.uniform(b_range[0], b_range[1])
        return a, b, func(sources, surface(a, b))


    with Pool() as pool:
        if mode == 'random':
            num_points = math.ceil(a_length * b_length * a_density ** 2)
            points = pool.map(eval_random_point, [0] * num_points)
        else:
            a_coords = np.linspace(a_range[0], a_range[1], a_length * a_density)
            b_coords = np.linspace(b_range[0], b_range[1], b_length * b_density)
            eval_points = list(itertools.product(a_coords, b_coords))
            points = pool.map(lambda p: (p[0], p[1], intensity_at(sources, surface(p[0], p[1]))), eval_points)

    return points


'''def eval_surface(sources, surface, a_range, b_range,
                 a_length='auto',
                 b_length='auto',
                 a_density=1,
                 b_density=1):
    points = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]

    a_coords = np.linspace(a_range[0], a_range[1], a_length * a_density)
    b_coords = np.linspace(b_range[0], b_range[1], b_length * b_density)
    eval_points = list(itertools.product(a_coords, b_coords))

    with Pool() as pool:
        points = pool.map(lambda p: (p[0], p[1], intensity_at(sources, surface(p[0], p[1]))), eval_points)

    # for a in np.linspace(a_range[0], a_range[1], a_length * a_density):
    #     for b in np.linspace(b_range[0], b_range[1], b_length * b_density):
    #         points.add((a, b, intensity_at(sources, surface(a, b))))
    return points'''


# TODO polarization
class Light:
    def __init__(self, source=(0, 0), frequency=RED_F, amplitude=1, phase_offset=0, velocity=C):
        """
        :param source: location (x, y) of source
        :param frequency: temporal frequency
        :param phase_offset: phase offset in radians (0 - 2*pi)
        :param velocity: propagation speed
        """
        self.source = np.asarray(source)
        self.phase_offset = phase_offset
        self.frequency = frequency
        self.amplitude = amplitude
        self.v = velocity
        self.wavelength = self.v / self.frequency
        self.k = 2 * math.pi / self.wavelength

    def change_frequency(self, new_frequency):
        self.frequency = new_frequency
        self.wavelength = self.v / self.frequency
        self.k = 2 * math.pi / self.wavelength

    def change_wavelength(self, new_wavelength):
        self.wavelength = new_wavelength
        self.frequency = self.v / self.wavelength
        self.k = 2 * math.pi / self.wavelength

    def phase_at(self, location):
        """
        returns phase angle (0 - 2 * pi)
        """
        r = self.path_length(location)
        return (self.k * r + self.phase_offset) % (2 * math.pi)

    def path_length(self, location):
        raise Exception("Not implemented")

    def detect(self, location):
        # todo scale by path length
        return self.amplitude, self.phase_at(location)


class PointSource(Light):
    def __init__(self, source=(0, 0), frequency=RED_F, amplitude=1, phase_offset=0, velocity=C):
        Light.__init__(self, source, frequency, amplitude, phase_offset, velocity)

    def path_length(self, location):
        return distance(self.source, location)

    def detect(self, location):
        return self.amplitude / self.path_length(location), self.phase_at(location)


class PlaneWave(Light):
    def __init__(self, source=(0, 0), frequency=RED_F, amplitude=1, phase_offset=0, direction=(1, 0), velocity=C):
        Light.__init__(self, source, frequency, amplitude, phase_offset, velocity)
        self.direction = np.asarray(direction)

    def path_length(self, location):
        return np.abs(np.dot(np.asarray(location) - self.source, self.direction) / np.linalg.norm(self.direction))


'''def intensity(sources, point):
    #check coherence
    if not sources[0].wavelength == sources[1].wavelength:
        print('incoherent')
        return
    init_phase_diff = sources[1].init_phase - sources[0].init_phase
    path_difference = sources[1].path_length(point) - sources[0].path_length(point)
    path_phase_diff = 2 * math.pi * path_difference / sources[1].wavelength
    phase_diff = init_phase_diff + path_phase_diff
    a = sources[0].amplitude
    b = sources[1].amplitude
    combined_amplitude = math.sqrt(a**2 + b**2 + 2*a*b*math.cos(phase_diff))
    return combined_amplitude**2'''
