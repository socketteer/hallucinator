import sys

sys.path.append('../ikonal')
import ikonal
import math
import numpy as np

frequency = 100
amplitude = 1

f = lambda u: amplitude * math.sin(frequency * u / (2 * np.pi))

source1 = ikonal.wave_2(f=f, v=1, source=(0, 0), falloff=0.5)

rect_region = lambda f: ikonal.rectangle_region(f=f,
                                                x_range=(-1, 1),
                                                y_range=(-2, 2),
                                                density=10)

region_points = rect_region(f=lambda x, y: source1(x, y, 0))

arr = ikonal.set_to_gradient(points=region_points, x_range=(-5, 5), y_range=(-5, 5), black_ref=-1.0,
                             white_ref=1.0, default=ikonal.BLUE, resolution=5)

ikonal.save_img(arr, 'path_region_test')

ikonal.video(frame_func=lambda t: ikonal.regional_gradient_frame(f=source1,
                                                                 t=t,
                                                                 region=rect_region,
                                                                 x_range=(-5, 5),
                                                                 y_range=(-5, 5),
                                                                 resolution=5,
                                                                 white_ref=1.0,
                                                                 black_ref=-1.0,
                                                                 default=ikonal.RED),
             filename='grad_path_vid_test',
             t_range=(1, 10),
             FPS=10)
