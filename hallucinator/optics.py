import math
import hallucinator as hl
import numpy as np
import random

#TODO integrate

class Light:
    def __init__(self, source, init_phase, wavelength, amplitude):
        self.source = np.asarray(source)
        self.init_phase = init_phase
        self.wavelength = wavelength
        self.amplitude = amplitude


class PointSource(Light):
    def __init__(self, source, wavelength, amplitude, init_phase):
        Light.__init__(self, source, init_phase, wavelength, amplitude)

    def path_length(self, point):
        return np.linalg.norm(point-self.source)


class PlaneWave(Light):
    def __init__(self, source, wavelength, amplitude, init_phase, direction):
        Light.__init__(self, source, init_phase, wavelength, amplitude)
        self.direction = np.asarray(direction)

    def path_length(self, point):
        return np.abs(np.dot(np.asarray(point) - self.source, self.direction) / np.linalg.norm(self.direction))


def intensity(sources, point):
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
    return combined_amplitude**2


def eval_surface_intensity(sources, surface, a_range, b_range,
                           a_length='auto',
                           b_length='auto',
                           a_density=1,
                           b_density=1):
    points = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]
    for a in np.linspace(a_range[0], a_range[1], a_length * a_density):
        for b in np.linspace(b_range[0], b_range[1], b_length * b_density):
            points.add((a, b, intensity(sources, surface(a, b))))

    return points


def eval_surface_intensity_random(sources, surface, a_range, b_range,
                           a_length='auto',
                           b_length='auto',
                           density=1):
    points = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]
    for _ in range(a_length * b_length * density):
        a = random.uniform(a_range[0], a_range[1])
        b = random.uniform(b_range[0], b_range[1])
        points.add((a, b, intensity(sources, surface(a, b))))
    return points

