# use object module in 2d
import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import random

surface = lambda a, b: (a, b)
source1 = hl.PointSource(source=(-0, 0))
planewave1 = hl.PlaneWave(source=(0, 0), direction=(0, 1))

a_range = (-5, 5)
b_range = (-5, 5)

intensities = hl.eval_surface(sources=[source1, planewave1],
                              surface=surface,
                              a_range=a_range,
                              b_range=b_range,
                              a_density=100,
                              b_density=100)

canv = hl.set_to_gradient(intensities,
                          x_range=a_range,
                          y_range=b_range,
                          black_ref=0,
                          white_ref=4.0,
                          default=hl.GRAY,
                          resolution=100)

hl.render_from_array(canv)
# hl.save_img(canv, 'two_point_stacked')
