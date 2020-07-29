import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def gen_spiral(location=(0, 0, 20), density=1, radius=1, turns=5, rotate_x=math.pi/4, camera_pos=(0, 0, 0)):
    scene = hl.MonochromeScene()

    spiral = lambda p: (math.cos(p * 2 * math.pi)*radius - location[0],
                        p/density - location[1],
                        math.sin(p * 2 * math.pi)*radius - location[2])

    spiral_obj = scene.add_object(hl.path_3(path_func=spiral,
                                            p_range=(0, turns),
                                            path_length=10 * math.pi).rotate(theta=rotate_x,
                                                                             axis=(1, 0, 0),
                                                                             p=location),
                                  name="coil")

    camera_position = np.matmul(hl.translate_3(camera_pos), hl.IDENTITY4)

    scene.render_scene(x_range=(-3, 3),
                       y_range=(-3, 3),
                       resolution=200,
                       camera_position=camera_position,
                       projection_type='weak',
                       density=100,
                       foreground=hl.WHITE,
                       background=hl.BLACK,
                       display=True)


gen_spiral(location=(0, 0, 20), density=5, radius=1, turns=10, rotate_x=math.pi/8, camera_pos=(0, 0, -20))
