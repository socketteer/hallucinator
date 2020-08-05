import hallucinator as hl
import types
from typing import TypedDict, NamedTuple, Tuple
import math


def wavy_surface(amplitude: float = 1,
            frequency: float = 1,
            direction: Tuple[float, float] = (0, 1),
            phase: float = 0,
            rotate_x: float = 0,
            location: Tuple[int, int, int] = (0, 0, 20)):
    surface_func = hl.plane_wave(amplitude, frequency, direction=direction, phase=phase)
    surface_obj = hl.ParaObject3(surface_func,
                                 region_type='2d',
                                 region_params={'surface_range': ((0, 10), (0, 10))},
                                 species='surface').rotate(theta=rotate_x, axis=(1, 0, 0)).translate(location)
    return surface_obj



scene = hl.MonochromeScene()
'''scene.add_object(wavy_surface(amplitude=1, frequency=2, direction=(1, 1), phase=0, rotate_x=0, location=(0, 0, 50)),
                 "surface")'''
scene.add_object(wavy_surface(amplitude=1, frequency=1, direction=(2, 1), phase=0, rotate_x=math.pi/4, location=(0, 0, 50)),
                 "surface2")


camscene = scene.render_scene(camera_position=(0, 0, 0),
                              projection_type='weak',
                              styles='uniform',
                              x_range=(-2, 12),
                              y_range=(-2, 12),
                              resolution=100,
                              density=(15, 15))

hl.render_from_array(camscene)