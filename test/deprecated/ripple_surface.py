import hallucinator as hl
from typing import Tuple
import math

scene = hl.MonochromeScene()

location = (0, 0, 20)
rotate_x = math.pi / 4
scene.add_object(hl.ParaObject3(hl.gen_ripple(amplitude=0.5, frequency=3, phase=0),
                                region_type='2d',
                                region_params={'surface_range': ((-10, 10), (-10, 10))},
                                species='surface').rotate(theta=rotate_x, axis=(1, 0, 0)).translate(location), "ripple")

camscene = scene.render_scene(camera_position=(0, -3, -50),
                              projection_type='weak',
                              styles='uniform',
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=50,
                              density=(10, 10))

hl.render_from_array(camscene)
