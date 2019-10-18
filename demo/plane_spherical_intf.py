import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def make_zone_plate(distance, wavelength, phase_diff, a_density, b_density, direction, x_range, y_range):
    surface = lambda a, b: (a, b, distance)
    source = (0, 0, 0)

    planewave = hl.PlaneWave(source=source, wavelength=wavelength, amplitude=1, init_phase=0, direction=direction)

    spherewave = hl.PointSource(source=source, wavelength=wavelength, amplitude=1, init_phase=phase_diff)

    points = hl.eval_surface_intensity(sources=(planewave, spherewave),
                                       surface=surface,
                                       a_range=x_range,
                                       b_range=y_range,
                                       a_density=a_density,
                                       b_density=b_density)

    canv = hl.set_to_gradient(points,
                              x_range=x_range,
                              y_range=y_range,
                              black_ref=0,
                              white_ref=4.0,
                              default=hl.GRAY,
                              resolution=30)

    return canv


distance = 20
wavelength = 0.1
phase_diff = 0
a_density = 30
b_density = 30
direction = (0, 0, 1)
x_range = (-20, 20)
y_range = (-20, 20)

zp = make_zone_plate(distance=distance,
                     wavelength=wavelength,
                     phase_diff=phase_diff,
                     a_density=a_density,
                     b_density=b_density,
                     direction=direction,
                     x_range=x_range,
                     y_range=y_range)

hl.render_from_array(zp)

hl.save_img(zp, 'zoneplates/zoneplate_d{0}-w{1}-p{2}-a{3}-b{4}-dir{5}-xr{6}-yr{7}'.format(distance, wavelength, phase_diff,
                                                      a_density, b_density, direction, x_range, y_range))

'''
hl.video(frame_func=lambda t: make_zone_plate(distance=distance,
                                              wavelength=wavelength,
                                              phase_diff=phase_diff,
                                              a_density=a_density,
                                              b_density=b_density*t,
                                              direction=direction),
         filename='zoneplates/zone_plate_change_b_density',
         t_range=(1, 5),
         FPS=10)'''
