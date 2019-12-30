# use object module in 2d
import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import random

surface = lambda a, b: (a, b)
source1 = hl.PointSource(source=(-0.001, 0))
source2 = hl.PointSource(source=(0.001, 0))
source3 = hl.PointSource(source=(0, 0))
source4 = hl.PointSource(source=(0, -100))

num_sources = 30
slit_width = 0.01
interval = slit_width / num_sources
line_of_sources = []
for i in range(num_sources):
    #phase = random.uniform(0, 2*math.pi)
    phase = 0
    line_of_sources.append(hl.PointSource(source=(0, -0.001 + i * interval), phase_offset=phase))


planewave1 = hl.PlaneWave(source=(0, 0), direction=(0, 1))
planewave2 = hl.PlaneWave(source=(0, 0), direction=(1, 0))

'''print(source1.path_length(location=(1, 1)))
print(planewave1.path_length(location=(1, 0)))
print(planewave1.path_length(location=(0, 1)))
print(planewave2.path_length(location=(1, 0)))
print(planewave2.path_length(location=(0, 1)))
print(source1.phase_at(location=(0, 0)))
print(source1.phase_at(location=(1, 0)))
print(source1.phase_at(location=(0.000000045, 0)))
print(source1.detect(location=(0, 0)))
print(source1.detect(location=(1, 0)))
print(hl.cart_to_polar(hl.field_at(sources=[source1], location=(0, 0))))
print(hl.cart_to_polar(hl.field_at(sources=[source1], location=(1, 0))))
print(hl.cart_to_polar(hl.field_at(sources=[source2], location=(1, 0))))
print(hl.intensity_at(sources=[source1], location=(1, 0)))
print(hl.intensity_at(sources=[source2], location=(1, 0)))
print(hl.intensity_at(sources=[source1, source2], location=(1, 0)))
print(hl.intensity_at(sources=[source1, source2], location=(1.01, 0)))'''

a_range = (-0.1, 1)
b_range = (-0.1, 1)

intensities = hl.eval_surface_intensity_random(sources=line_of_sources,
                                               surface=surface,
                                               a_range=a_range,
                                               b_range=b_range,
                                               density=400)
canv = hl.set_to_gradient(intensities,
                          x_range=a_range,
                          y_range=b_range,
                          black_ref=0,
                          white_ref=4.0,
                          default=hl.GRAY,
                          resolution=400)

hl.render_from_array(canv)
hl.save_img(canv, 'width{0}_{1}-points_random'.format(slit_width, num_sources))
#hl.save_img(canv, 'two_point_stacked')

