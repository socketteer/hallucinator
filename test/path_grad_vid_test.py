import sys
sys.path.append('../ikonal')
import ikonal
import math
import numpy as np


frequency = 100
amplitude = 1

f = lambda u: amplitude * math.sin(frequency * u / (2 * np.pi))

source1 = ikonal.wave_2(f, v=1, source=(0, 0), falloff=0.5)

ikonal.video(frame_func=lambda t: ikonal.selective_gradient_frame(func=source1,
                                                                  t=t,
                                                                  path=lambda p: (3, p),
                                                                  p_range=[-5, 5],
                                                                  density=10,
                                                                  x_range=(-10,10),
                                                                  y_range=(-10,10),
                                                                  resolution=5,
                                                                  white_ref=1.0,
                                                                  black_ref=-1.0,
                                                                  default=ikonal.RED),
             filename='grad_path_vid_test',
             t_range=(1, 10),
             FPS=10)

