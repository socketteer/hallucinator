import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def plane_interference(distance, wavelength, phase_diff, sampling_density, a_direction, b_direction):
    surface = lambda a, b: (a, b, distance)
    source1 = (0, 0, 0)
    source2 = (0, 0, 0)

    pin1 = hl.PlaneWave(source=source1, wavelength=wavelength, amplitude=1, init_phase=0, direction=a_direction)

    pin2 = hl.PlaneWave(source=source2, wavelength=wavelength, amplitude=1, init_phase=phase_diff,
                        direction=b_direction)

    points = hl.eval_surface_intensity(sources=(pin1, pin2),
                                       surface=surface,
                                       a_range=(-15, 15),
                                       b_range=(-15, 15),
                                       a_density=sampling_density,
                                       b_density=sampling_density)

    canv = hl.set_to_gradient(points,
                              x_range=(-15, 15),
                              y_range=(-15, 15),
                              black_ref=0,
                              white_ref=4.0,
                              default=hl.GRAY,
                              resolution=50)

    return canv


angle = math.pi / 180
a_direction = (0, math.sin(angle), math.cos(angle))
b_direction = (0, -math.sin(angle), math.cos(angle))
distance = 10
wavelength = 0.1
phase_diff = 0

canv = plane_interference(distance=distance,
                          wavelength=wavelength,
                          phase_diff=phase_diff,
                          sampling_density=20,
                          a_direction=a_direction,
                          b_direction=b_direction)

hl.render_from_array(canv)
hl.save_img(canv, 'planewaves/planewaves_{0}-w{1}-p{2}-a{3}'.format(distance, wavelength, phase_diff,
                                                                    angle))

