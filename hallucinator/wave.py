import numpy as np
import hallucinator as hal
import math
import operator


def propagating_disturbance(f, v):
    return lambda p, t: f(p - v * t)


# TODO 2d propagate in both directions


def propagating_disturbance_2d(f, v):
    return lambda a, b, t: f(hal.pnorm(2)((a, b)) - v * t)


def damped_harmonic(amplitude, frequency, damping_coeff):
    return lambda u: 0 if u > 0 else hal.sin_wave(amplitude=amplitude, frequency=frequency)(u) \
                                     * math.exp(u * damping_coeff)


def harmonic(amplitude, wavelength, frequency):
    k = 2 * math.pi / wavelength
    v = frequency * wavelength
    return lambda p, t: (p, amplitude * math.sin(k * (p - v * t)))


def sin_wave(amplitude, frequency):
    return lambda u: amplitude * math.sin(u * frequency)


def wave_2(f, v, source=(0, 0), falloff=0, starttime='eternal', defaultval=0):
    func = lambda a, b, t: (a, b, f(math.sqrt((source[0] - a) ** 2 + (source[1] - b) ** 2) - v * t)
                            * np.e ** (-falloff * math.sqrt((source[0] - a) ** 2 + (source[1] - b) ** 2)))
    if starttime == 'eternal':
        return func
    else:
        return lambda a, b, t: (a, b, defaultval) if t < starttime else func(a, b, (t - starttime))


def superposition(f1, f2):
    return lambda x, y, t: tuple(map(operator.add, f1(x, y, t), f2(x, y, t)))

