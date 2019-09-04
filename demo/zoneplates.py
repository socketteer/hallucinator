import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def make_zone_plate(distance, wavelength, phase_diff, a_density, b_density, direction):
    surface = lambda a, b: (a, b, distance)
    source = (0, 0, 0)

    planewave = hl.PlaneWave(source=source, wavelength=wavelength, amplitude=1, init_phase=0, direction=direction)

    spherewave = hl.PointSource(source=source, wavelength=wavelength, amplitude=1, init_phase=phase_diff)

    points = hl.eval_surface_intensity(sources=(planewave, spherewave),
                                       surface=surface,
                                       a_range=(-20, 20),
                                       b_range=(-20, 20),
                                       a_density=a_density,
                                       b_density=b_density)

    canv = hl.set_to_gradient(points,
                              x_range=(-20, 20),
                              y_range=(-20, 20),
                              black_ref=0,
                              white_ref=4.0,
                              default=hl.GRAY,
                              resolution=50)

    return canv


distance = 15
wavelength = 0.01
phase_diff = 0
a_density = 40
b_density = 40
direction = (0, 0, 1)

zp = make_zone_plate(distance=distance,
                     wavelength=wavelength,
                     phase_diff=phase_diff,
                     a_density=a_density,
                     b_density=b_density,
                     direction=direction)

hl.render_from_array(zp)

hl.save_img(zp, 'zoneplates/zoneplate_d{0}-w{1}-p{2}-a{3}-b{4}-dir{5}'.format(distance, wavelength, phase_diff,
                                                         a_density, b_density, direction))

'''hl.video(frame_func=lambda t: make_zone_plate(distance=15,
                                              wavelength=0.1,
                                              phase_diff=0,
                                              sampling_density=15),
         filename='zone_plate_change_sample_rate_5',
         t_range=(2, 6),
         FPS=10)'''
