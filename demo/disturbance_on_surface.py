import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np

scene = hl.MonochromeScene()

f = hl.damped_harmonic(amplitude=1, frequency=5, damping_coeff=0.8)
disturbance = hl.propagating_disturbance_2d(f, v=2)

surface = hl.disturbance_on_surface(disturbance=disturbance,
                                    init_pos=(0, 3),
                                    polarization=(-1, 0, 0),
                                    surface=hl.plane(p0=(0, 0, 0),
                                                     v1=(0, 1, 0),
                                                     v2=(0, 0, 1)),
                                    a_range=(-5, 5),
                                    b_range=(-5, 5))

scene.add_object(surface, name="basin")

camera_pos = hl.IDENTITY4
camera_pos = np.matmul(camera_pos, hl.translate_3(-5, 0, -15))
camera_pos = np.matmul(camera_pos, hl.rotate_3(math.pi / 3, axis=(0, 1, 0)))

hl.video(frame_func=lambda t: scene.render_scene(params={'basin': {'t': t}},
                                                 x_range=(-20, 20),
                                                 y_range=(-20, 20),
                                                 camera_position=camera_pos,
                                                 resolution=50,
                                                 projection_type="weak",
                                                 style='line',
                                                 region_params={'a_spacing': 0.3,
                                                                'b_spacing': 0.3},
                                                 foreground=hl.WHITE,
                                                 background=hl.BLACK,
                                                 display=False),
         filename='disturbance_on_surface_test_refactor',
         t_range=(0, 5),
         FPS=10)
