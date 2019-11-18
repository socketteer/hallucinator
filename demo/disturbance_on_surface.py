import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np

scene = hl.MonochromeScene()

f = hl.damped_harmonic(amplitude=0.4, frequency=10, damping_coeff=-0.2)

disturbance = hl.propagating_disturbance_2d(f, v=2)

surface = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                           v1=(0, 1, 0),
                                           v2=(0, 0, 1)),
                     a_range=(-5, 5),
                     b_range=(-5, 5))

'''surface.add_disturbance(disturbance=disturbance,
                        init_pos=(3, 0),
                        polarization=(-1, 0, 0),
                        start_time=2)

surface.add_more_disturbances(disturbance=disturbance,
                              init_pos=(-3, 0),
                              polarization=(-1, 0, 0),
                              start_time=3)'''

scene.add_object(surface, name="basin")

x_transl = 0
y_transl = 0
z_transl = 10

camera_pos = hl.IDENTITY4


def rotate(theta, axis):
    return np.matmul(camera_pos, hl.rotate_3(theta, axis))


translate = np.matmul(camera_pos, hl.translate_3(x_transl, y_transl, z_transl))

'''params={'basin': {'t': t}},'''
hl.video2(frame_function=lambda t: scene.render_scene(x_range=(-25, 25),
                                                      y_range=(-25, 25),
                                                      camera_position=np.matmul(np.matmul(np.matmul(camera_pos,
                                                                                                rotate(
                                                                                                    theta=t * math.pi / 10,
                                                                                                    axis=(1, 0, 0))),
                                                                                      rotate(math.pi / 6, (0, 1, 0))),
                                                                            translate),
                                                      resolution=50,
                                                      projection_type="weak",
                                                      style='line',
                                                      region_params={'a_spacing': 0.2,
                                                                 'b_spacing': 0.2,
                                                                 'toggle_b': False},
                                                      foreground=hl.WHITE,
                                                      background=hl.BLACK,
                                                      display=False),
          filename='surface_test_rotate',
          frame_arguments=np.linspace(0, 10, 70),
          fps=7,
          parallel=True)
