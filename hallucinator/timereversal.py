import numexpr as ne
import hallucinator as hl
import numpy as np
import math


# make more general and move
def field(sources, t=0, value_range=(-10, 10), resolution=16):
    source_planes = []
    xy = hl.xy_plane(value_range=value_range, resolution=resolution)

    for s in sources:
        source_planes.append(source(xy=xy, t=t, **s))
    source_planes = np.array(source_planes)
    total = ne.evaluate("sum(source_planes, axis=2)")
    return total, source_planes


def polar_field(comp_field):
    real_field = comp_field[0]
    imag_field = comp_field[1]
    p_2 = math.pi / 2
    theta = ne.evaluate("arctan2(real_field, imag_field) + p_2 + (p_2 * (real_field) / (-real_field))")
    amplitude2 = ne.evaluate("real_field**2 + imag_field**2")
    amplitude = ne.evaluate("sqrt(amplitude2)")
    return theta, amplitude


def source(xy, t=0, position=(0, 0), k=1, amplitude=1, ang_freq=1, phase=(0, 0)):
    r2 = ne.evaluate("sum((xy-position)**2, axis=2)")
    r = ne.evaluate("sqrt(r2)")
    real_phase = phase[0]
    imag_phase = phase[1]
    reals = ne.evaluate("amplitude * cos(k * r - ang_freq * t + real_phase)")
    complexes = ne.evaluate("amplitude * sin(k * r - ang_freq * t + imag_phase)")

    return reals, complexes


sources = [{'position': (0, -10)}, {'position': (0, 10)}]
spos, fields = field(sources, t=0)
print('superposition:')
print(spos)
print('fields:')
print(fields)
phase_field, _ = polar_field(spos)
print(phase_field)