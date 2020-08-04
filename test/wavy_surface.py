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
                                 region_params={'a_range': (-5, 5),
                                                'b_range': (-5, 5),
                                                'a_length': 'auto',
                                                'b_length': 'auto'},
                                 species='surface').rotate(theta=rotate_x, axis=(1, 0, 0)).translate(location)
    return surface_obj



scene = hl.MonochromeScene()
scene.add_object(wavy_surface(amplitude=1, frequency=2, direction=(1, 1), phase=0, rotate_x=math.pi/4, location=(0, 0, 50)),
                 "surface")
camscene = hl.camscene(scene, camera_pos=(0, 0, 0),
                       render_density=100,
                       projection_type='weak',
                       styles='line',
                       x_range=(-10, 10),
                       y_range=(-10, 10),
                       resolution=200,
                       a_spacing=1,
                       b_spacing=1)
hl.render_from_array(camscene)