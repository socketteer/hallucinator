import sys
from typing import Tuple

sys.path.append('../hallucinator')
import hallucinator as hl
import math


def gen_spiral(location: Tuple[int, int, int] = (0, 0, 20),
               coil_density: float = 1,
               radius: float = 1,
               turns: float = 5,
               rotate_x: float = math.pi/4,
               camera_pos: Tuple[int, int, int] = (0, 0, 0)):

    spiral = lambda p: (math.cos(p * 2 * math.pi)*radius - location[0],
                        p/coil_density - location[1],
                        math.sin(p * 2 * math.pi)*radius - location[2])

    spiral_obj = hl.path_3(path_func=spiral,
                           p_range=(0, turns),
                           path_length=10 * math.pi).translate(location).rotate(theta=rotate_x,
                                                                                axis=(1, 0, 0),
                                                                                p=location)
    return spiral_obj

resolution = 200
x_range = (-3, 3)
y_range = (-3, 3)
projection_type = 'weak'
render_density = 100
scene = hl.MonochromeScene()
scene.add_object(gen_spiral(location=(0, 0, 20),
                            coil_density=2,
                            radius=2,
                            turns=20,
                            rotate_x=0,
                            camera_pos=(0, 0, -10)), "spiral")

camscene = scene.render_scene(camera_position=(0, 0, 0),
                              projection_type='weak',
                              styles='path',
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=50,
                              density=50)
hl.render_from_array(camscene)