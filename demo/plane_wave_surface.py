import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np

scene = hl.MonochromeScene()

f = hl.sin_wave(amplitude=0.4, frequency=3)

disturbance = hl.plane_wave(f, v=2, direction=(1, 0))

surface = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                           v1=(0, 1, 0),
                                           v2=(0, 0, 1)),
                     a_range=(-10, 10),
                     b_range=(-10, 10))

surface.add_disturbance(disturbance=disturbance,
                        init_pos=(3, 0),
                        polarization=(-1, 0, 0),
                        start_time=0)

scene.add_object(surface, name="basin")

x_transl = 0
y_transl = 0
z_transl = 10

camera_pos = hl.IDENTITY4


def rotate(theta, axis):
    return np.matmul(camera_pos, hl.rotate_3(theta, axis))


translate = np.matmul(camera_pos, hl.translate_3(x_transl, y_transl, z_transl))

hl.video2(frame_function=lambda t: scene.render_scene(params={'basin': {'t': t}},
                                                      x_range=(-20, 20),
                                                      y_range=(-20, 20),
                                                      camera_position=np.matmul(np.matmul(np.matmul(camera_pos,
                                                                                                rotate(
                                                                                                    theta=t * math.pi / 10,
                                                                                                    axis=(1, 0, 0))),
                                                                                      rotate(math.pi / 8, (0, 1, 0))),
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
          filename='./videos/plane_wave',
          frame_arguments=np.linspace(0, 10, 50),
          fps=7,
          parallel=True)