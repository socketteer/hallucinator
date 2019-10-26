import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np
import random

scene = hl.MonochromeScene()

f = hl.damped_harmonic(amplitude=0.02, frequency=30, damping_coeff=0.9)
disturbance = hl.propagating_disturbance_2d(f, v=0.5)

surface = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                           v1=(0, 1, 0),
                                           v2=(0, 0, 1)),
                     a_range=(-5, 5),
                     b_range=(-5, 5))

num_drops = 20
drops = []
surface.add_disturbance(disturbance=disturbance,
                        init_pos=(random.uniform(-5, 5), random.uniform(-5, 5)),
                        polarization=(-1, 0, 0),
                        start_time=random.uniform(0, 10))

for i in range(num_drops):
    start_time = random.uniform(0, 10)
    x_location = random.uniform(-5, 5)
    y_location = random.uniform(-5, 5)
    surface.add_more_disturbances(disturbance=disturbance,
                                  init_pos=(x_location, y_location),
                                  polarization=(-1, 0, 0),
                                  start_time=start_time)

scene.add_object(surface, name="basin")

camera_pos = hl.IDENTITY4
camera_pos = np.matmul(camera_pos, hl.translate_3(-5, 0, -15))
camera_pos = np.matmul(camera_pos, hl.rotate_3(math.pi / 3, axis=(0, 1, 0)))

hl.video(frame_func=lambda t: scene.render_scene(params={'basin': {'t': t}},
                                                 x_range=(-25, 25),
                                                 y_range=(-25, 25),
                                                 camera_position=camera_pos,
                                                 resolution=50,
                                                 projection_type="weak",
                                                 style='line',
                                                 region_params={'a_spacing': 0.1,
                                                                'b_spacing': 0.1},
                                                 foreground=hl.WHITE,
                                                 background=hl.BLACK,
                                                 display=False),
         filename='rain',
         t_range=(0, 10),
         FPS=5)
