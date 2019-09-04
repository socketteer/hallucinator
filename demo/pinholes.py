import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def make_pinholes(distance, wavelength, phase_diff, sampling_density, separation):
    surface = lambda a, b: (a, b, distance)
    source1 = (-separation, 0, 0)
    source2 = (separation, 0, 0)

    pin1 = hl.PointSource(source=source1, wavelength=wavelength, amplitude=1, init_phase=0)

    pin2 = hl.PointSource(source=source2, wavelength=wavelength, amplitude=1, init_phase=phase_diff)

    points = hl.eval_surface_intensity(sources=(pin1, pin2),
                                       surface=surface,
                                       a_range=(-30, 30),
                                       b_range=(-30, 30),
                                       a_density=sampling_density,
                                       b_density=sampling_density)

    canv = hl.set_to_gradient(points,
                              x_range=(-30, 30),
                              y_range=(-30, 30),
                              black_ref=0,
                              white_ref=4.0,
                              default=hl.GRAY,
                              resolution=50)

    return canv


'''canv = make_pinholes(distance=10,
                     wavelength=0.001,
                     phase_diff=0,
                     sampling_density=20,
                     separation=0.1)

hl.render_from_array(canv)
hl.save_img(canv, 'two_pinhole_d10-w0.001-s0.1-sd20')'''


hl.video(frame_func=lambda t: make_pinholes(distance=10,
                                            wavelength=0.001,
                                            phase_diff=0,
                                            sampling_density=t**2,
                                            separation=0.1),
         filename='pinholes_2',
         t_range=(0, 7),
         FPS=5)

