import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def make_pinholes(distance, wavelength, phase_diff, sampling_density, separation):
    surface = lambda a, b: (a, b, distance)
    source1 = (0, 0, 0)
    source2 = (separation, 0, 0)

    pin1 = hl.PointSource(source=source1, wavelength=wavelength, amplitude=1, init_phase=0)

    pin2 = hl.PointSource(source=source2, wavelength=wavelength, amplitude=1, init_phase=phase_diff)

    points = hl.eval_surface_intensity(sources=(pin1, pin2),
                                       surface=surface,
                                       a_range=(-50, 50),
                                       b_range=(-50, 50),
                                       density=sampling_density)

    canv = hl.set_to_gradient(points,
                              x_range=(-50, 50),
                              y_range=(-50, 50),
                              black_ref=0,
                              white_ref=4.0,
                              default=hl.GRAY,
                              resolution=10)

    return canv


canv = make_pinholes(distance=10,
                     wavelength=0.001,
                     phase_diff=0,
                     sampling_density=5,
                     separation=0.01)

hl.render_from_array(canv)
hl.save_img(canv, 'two_pinhole_d10-w0.001-s0.01')

'''
hl.video(frame_func=lambda t: make_pinholes(distance=t,
                                            wavelength=0.1,
                                            phase_diff=0,
                                            sampling_density=5),
         filename='zone_plate_change_distance_lower_density',
         t_range=(10, 25),
         FPS=5)
'''
