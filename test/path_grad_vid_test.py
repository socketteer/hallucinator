import sys
sys.path.append('../ikonal')
import ikonal
import math
import numpy as np

frequency = 100
amplitude = 1

f = lambda u: amplitude * math.sin(frequency * u / (2 * np.pi))

source1 = ikonal.wave_2(f=f, v=1, source=(0, 0), falloff=0.5)

rect_region = lambda fu: ikonal.rectangle_region(f=fu,
                                                 x_range=(-1, 1),
                                                 y_range=(-2, 2),
                                                 density=10)

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
