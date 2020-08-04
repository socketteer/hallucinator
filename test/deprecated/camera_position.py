import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import numpy as np
import math

scene = hl.MonochromeScene()

scene.add_object(hl.box(10, 10, 10), name='box')
scene.add_object(hl.box(10, 10, 10, p0=(0, 20, 20)), name='box2')
scene.add_object(hl.box(10, 10, 10, p0=(20, 0, 20)), name='box3')
scene.add_object(hl.box(10, 10, 10, p0=(0, 0, 40)), name='box4')


#scene.render_scene(x_range=(-40, 80), y_range=(-40, 80), display=True, resolution=10)

scene = scene.transform(hl.translate_3(-20, -20, 50))

scene.render_scene(x_range=(-40, 40), y_range=(-40, 40), projection_type='weak', display=True, resolution=15)

camera_position = hl.IDENTITY4

scene.render_scene(x_range=(-40, 40), y_range=(-40, 40),
                   camera_position=camera_position,
                   projection_type='weak',
                   display=True,
                   resolution=15)

camera_position = np.matmul(hl.translate_3(20, 20, 20), camera_position)

scene.render_scene(x_range=(-40, 40), y_range=(-40, 40),
                   camera_position=camera_position,
                   projection_type='weak',
                   display=True,
                   resolution=15)

camera_position = np.matmul(hl.rotate_about_3(theta=-math.pi / 8, axis=(0, 1, 0), p=(20, 20, 20)), camera_position)


scene.render_scene(x_range=(-40, 40), y_range=(-40, 40),
                   camera_position=camera_position,
                   projection_type='weak',
                   display=True,
                   resolution=15)

camera_position = np.matmul(hl.rotate_about_3(theta=math.pi / 8, axis=(1, 0, 0), p=(20, 20, 20)), camera_position)

scene.render_scene(x_range=(-40, 40), y_range=(-40, 40),
                   camera_position=camera_position,
                   projection_type='weak',
                   display=True,
                   resolution=15)
