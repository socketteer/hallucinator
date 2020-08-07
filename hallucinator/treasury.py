import math
import numpy as np
import numexpr as ne
from typing import TypedDict, NamedTuple, Tuple


def wave(p, r, amp, f, phase):
    z = ne.evaluate("amp * sin(r * f + phase)")
    z = z.reshape((z.shape[0] * z.shape[1]))
    p = p.reshape((p.shape[0] * p.shape[1], 2)).transpose()
    return np.array([p[0], p[1], z])


def gen_spiral(coil_density: float = 1, radius: float = 1):

    def spiral(p):
        r = radius
        c = coil_density
        tau = 2 * math.pi
        x = ne.evaluate("cos(p * tau) * r")
        y = ne.evaluate("p /  c")
        z = ne.evaluate("sin(p * tau) * r")
        return np.array([x, y, z])

    return spiral


def gen_plane_wave(amplitude: float = 1,
                   frequency: float = 1,
                   direction: Tuple[float, float] = (0, 1),
                   phase: float = 0):

    def plane_wave(p):
        amp = amplitude
        f = frequency
        d = direction
        ph = phase
        r = ne.evaluate("sum(p * direction, axis=2)")
        return wave(p, r, amp, f, phase)

    return plane_wave


def gen_ripple(amplitude: float = 1,
               frequency: float = 1,
               phase: float = 0):

    def ripple(p):
        amp = amplitude
        f = frequency
        ph = phase
        x2y2 = ne.evaluate("sum(p**2, axis=2)")
        r = ne.evaluate("sqrt(x2y2)")
        return wave(p, r, amp, f, phase)

    return ripple
