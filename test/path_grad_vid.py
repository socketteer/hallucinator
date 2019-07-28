import sys
sys.path.append('../hallucinator')
import hallucinator
import math
import numpy as np

frequency = 100
amplitude = 1

f = lambda u: amplitude * math.sin(frequency * u / (2 * np.pi))

source1 = hallucinator.wave_2(f=f, v=1, source=(0, 0), falloff=0.5)

rect_region = lambda fu: hallucinator.surface_region(f=fu,
                                                     x_range=(-1, 1),
                                                     y_range=(-2, 2),
                                                     density=10)



hallucinator.video(frame_func=lambda t: hallucinator.regional_gradient_frame(f=source1,
                                                                             t=t,
                                                                             region=rect_region,
                                                                             x_range=(-5, 5),
                                                                             y_range=(-5, 5),
                                                                             resolution=5,
                                                                             white_ref=1.0,
                                                                             black_ref=-1.0,
                                                                             default=hallucinator.RED),
                   filename='grad_path_vid_test',
                   t_range=(1, 10),
                   FPS=10)
