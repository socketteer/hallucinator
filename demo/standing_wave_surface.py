import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np

scene = hl.MonochromeScene()

f = hl.sin_wave(amplitude=0.1, frequency=1)
f2 = hl.sin_wave(amplitude=0.1, frequency=2)
f3 = hl.sin_wave(amplitude=0.1, frequency=3)
f4 = hl.sin_wave(amplitude=0.1, frequency=4)

disturbance = hl.plane_wave(f, v=0.5, direction=(1, 0))
disturbance2 = hl.plane_wave(f2, v=0.5, direction=(-1, 0))
disturbance3 = hl.plane_wave(f3, v=0.5, direction=(1, 0))
disturbance4 = hl.plane_wave(f4, v=0.5, direction=(-1, 0))
disturbance5 = hl.plane_wave(f, v=0.5, direction=(0, 1))
disturbance6 = hl.plane_wave(f2, v=0.5, direction=(0, -1))
disturbance7 = hl.plane_wave(f3, v=0.5, direction=(0, 1))
disturbance8 = hl.plane_wave(f4, v=0.5, direction=(0, -1))


surface = hl.surface(surface_func=hl.plane(p0=(0, 0, 0),
                                           v1=(0, 1, 0),
                                           v2=(0, 0, 1)),
                     a_range=(-5, 5),
                     b_range=(-5, 5))

surface.add_disturbance(disturbance=disturbance,
                        init_pos=(3, 0),
                        polarization=(-1, 0, 0),
                        start_time=0)

surface.add_more_disturbances(disturbance=disturbance2,
                              init_pos=(-3, 0),
                              polarization=(-1, 0, 0),
                              start_time=0)

surface.add_more_disturbances(disturbance=disturbance3,
                              init_pos=(-3, 0),
                              polarization=(-1, 0, 0),
                              start_time=0)


surface.add_more_disturbances(disturbance=disturbance4,
                              init_pos=(-3, 0),
                              polarization=(-1, 0, 0),
                              start_time=0)

surface.add_more_disturbances(disturbance=disturbance5,
                              init_pos=(-3, 0),
                              polarization=(-1, 0, 0),
                              start_time=0)
surface.add_more_disturbances(disturbance=disturbance6,
                              init_pos=(-3, 0),
                              polarization=(-1, 0, 0),
                              start_time=0)
surface.add_more_disturbances(disturbance=disturbance7,
                              init_pos=(-3, 0),
                              polarization=(-1, 0, 0),
                              start_time=0)
surface.add_more_disturbances(disturbance=disturbance8,
                              init_pos=(-3, 0),
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

camera_pos = np.matmul(rotate(math.pi / 4, (0, 1, 0)), translate)

hl.video2(frame_func=lambda t: scene.render_scene(params={'basin': {'t': t}},
                                                  x_range=(-25, 25),
                                                  y_range=(-25, 25),
                                                  camera_position=camera_pos,
                                                  resolution=50,
                                                  projection_type="weak",
                                                  style='line',
                                                  region_params={'a_spacing': 0.2,
                                                                 'b_spacing': 0.2,
                                                                 'toggle_b': False},
                                                  foreground=hl.WHITE,
                                                  background=hl.BLACK,
                                                  display=False),
          filename='./videos/standing_wave_harmonics_2d',
          frame_arguments=np.linspace(0, 20, 50),
          fps=7,
          parallel=True)