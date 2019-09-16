import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def make_zone_plate(distance, wavelength, phase_diff, density, direction):
    surface = lambda a, b: (a, b, distance)
    source = (0, 0, 0)

    planewave = hl.PlaneWave(source=source, wavelength=wavelength, amplitude=1, init_phase=0, direction=direction)

    spherewave = hl.PointSource(source=source, wavelength=wavelength, amplitude=1, init_phase=phase_diff)

    points = hl.eval_surface_intensity_random(sources=(planewave, spherewave),
                                              surface=surface,
                                              a_range=(-15, 15),
                                              b_range=(-15, 15),
                                              density=density)

    canv = hl.set_to_gradient(points,
                              x_range=(-15, 15),
                              y_range=(-15, 15),
                              black_ref=0,
                              white_ref=4.0,
                              default=hl.GRAY,
                              resolution=50)

    return canv


distance = 15
wavelength = 0.05
phase_diff = 0
density = 300
direction = (0, 0, 1)

zp = make_zone_plate(distance=distance,
                     wavelength=wavelength,
                     phase_diff=phase_diff,
                     density=density,
                     direction=direction)

hl.render_from_array(zp)

hl.save_img(zp, 'zoneplates/zoneplate_rand_d{0}-w{1}-p{2}-d{3}-dir{4}'.format(distance, wavelength, phase_diff,
                                                                         density, direction))

'''hl.video(frame_func=lambda t: make_zone_plate(distance=15,
                                              wavelength=0.1,
                                              phase_diff=0,
                                              sampling_density=15),
         filename='zone_plate_change_sample_rate_5',
         t_range=(2, 6),
         FPS=10)'''
