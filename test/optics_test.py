import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np

surface = lambda a, b: (a, b, 10)
source = (0, 0, 0)
direction = (0, 0, 1)

planewave = hl.PlaneWave(source=source, wavelength=0.05, amplitude=1, init_phase=0, direction=direction)

spherewave = hl.PointSource(source=source, wavelength=0.05, amplitude=1, init_phase=math.pi/2)

points = hl.eval_surface_intensity(sources=(planewave, spherewave),
                                   surface=surface,
                                   a_range=(-15, 15),
                                   b_range=(-15, 15),
                                   density=15)

canv = hl.set_to_gradient(points,
                          x_range=(-15, 15),
                          y_range=(-15, 15),
                          black_ref=0,
                          white_ref=4.0,
                          default=hl.GRAY,
                          resolution=50)

hl.render_from_array(canv)
hl.save_img(canv, 'w0.05-d10-15-15-p0.5pi')