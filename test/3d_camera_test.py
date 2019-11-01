import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np
import random

scene = hl.MonochromeScene()

yz = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                      v1=(0, 1, 0),
                                      v2=(0, 0, 1)),
                a_range=(-5, 5),
                b_range=(-5, 5))

xy = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                      v1=(0, 1, 0),
                                      v2=(1, 0, 0)),
                a_range=(-5, 5),
                b_range=(-5, 5))

xz = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                      v1=(0, 0, 1),
                                      v2=(1, 0, 0)),
                a_range=(-5, 5),
                b_range=(-5, 5))

scene.add_object(xy, name="xy")
scene.add_object(yz, name="yz")
scene.add_object(xz, name="xz")

x_transl = 0
y_transl = 0
z_transl = 15

camera_pos = hl.IDENTITY4


def rotate(theta, axis):
    return np.matmul(camera_pos, hl.rotate_3(theta, axis))


translate = np.matmul(camera_pos, hl.translate_3(x_transl, y_transl, z_transl))

'''scene.render_scene(x_range=(-25, 25),
                   y_range=(-25, 25),
                   camera_position=camera_pos,
                   resolution=50,
                   projection_type="weak",
                   style='line',
                   region_params={'a_spacing': 0.5,
                                  'b_spacing': 0.5},
                   foreground=hl.WHITE,
                   background=hl.BLACK,
                   display=True)'''

hl.video(frame_func=lambda t: scene.render_scene(params={'basin': {'t': t}},
                                                 x_range=(-25, 25),
                                                 y_range=(-25, 25),
                                                 camera_position=np.matmul(np.matmul(camera_pos,
                                                                                     rotate(theta=t * math.pi / 5,
                                                                                            axis=(0, 1, 0) if t < 2.5
                                                                                            else ((0, 0, 1) if t < 5
                                                                                                  else (1, 0, 0)))),
                                                                           translate),
                                                 resolution=50,
                                                 projection_type="weak",
                                                 style='line',
                                                 region_params={'a_spacing': 1,
                                                                'b_spacing': 1},
                                                 foreground=hl.WHITE,
                                                 background=hl.BLACK,
                                                 display=False),
         filename='camera_rotate_test',
         t_range=(0, 7.5),
         FPS=7)
