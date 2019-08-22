import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def make_zone_plate(distance, wavelength, phase_diff, sampling_density):
    surface = lambda a, b: (a, b, distance)
    source = (0, 0, 0)
    direction = (0, 0, 1)

    planewave = hl.PlaneWave(source=source, wavelength=wavelength, amplitude=1, init_phase=0, direction=direction)

    spherewave = hl.PointSource(source=source, wavelength=wavelength, amplitude=1, init_phase=phase_diff)

    points = hl.eval_surface_intensity(sources=(planewave, spherewave),
                                       surface=surface,
                                       a_range=(-20, 20),
                                       b_range=(-20, 20),
                                       density=sampling_density)

    canv = hl.set_to_gradient(points,
                              x_range=(-20, 20),
                              y_range=(-20, 20),
                              black_ref=0,
                              white_ref=4.0,
                              default=hl.GRAY,
                              resolution=10)

    return canv


hl.video(frame_func=lambda t: make_zone_plate(distance=t*25,
                                              wavelength=0.05,
                                              phase_diff=0,
                                              sampling_density=5),
         filename='zone_plate_change_distance_25-200_w0.05',
         t_range=(1, 8),
         FPS=2)
