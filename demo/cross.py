import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np

scene = hl.MonochromeScene()

f = hl.sin_wave(amplitude=0.3, frequency=6)

disturbance = hl.propagating_disturbance_2d(f, v=2)

surface = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                           v1=(0, 1, 0),
                                           v2=(0, 0, 1)),
                     a_range=(-5, 5),
                     b_range=(-5, 5))

surface.add_disturbance(disturbance=disturbance,
                        init_pos=(0, 0),
                        polarization=(-1, 0, 0))

scene.add_object(hl.cross(width=1, depth=1, span=2, l_height=4, u_height=2, origin=(0, 0, 0)),
                 name="cross")

scene.add_object(surface, name="basin")

x_transl = 0
y_transl = 0
z_transl = 10

camera_pos = hl.IDENTITY4


def rotate(theta, axis):
    return np.matmul(camera_pos, hl.rotate_3(theta, axis))


translate = np.matmul(camera_pos, hl.translate_3(x_transl, y_transl, z_transl))


def frame(t, scene):
    return scene.render_scene(params={'basin': {'t': t}},
                              x_range=(-25, 25),
                              y_range=(-25, 25),
                              camera_position=np.matmul(np.matmul(camera_pos,
                                                                  rotate(math.pi / 6, (0, 1, 0))),
                                                        translate),
                              resolution=50,
                              projection_type="weak",
                              styles={'basin': 'line'},
                              region_params={'basin': {'a_spacing': 0.2,
                                                       'b_spacing': 0.2,
                                                       'toggle_b': False}},
                              foreground=hl.WHITE,
                              background=hl.RED,
                              display=False)


hl.video2(frame_function=lambda t: frame(t, scene),
          filename='./videos/cross',
          frame_arguments=np.linspace(0, 10, 70),
          fps=7,
          parallel=True)

'''hl.video(frame_func=lambda t: frame(t, scene),
         filename='crosstest',
         t_range=(0, 10),
         FPS=20)'''
