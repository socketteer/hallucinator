from typing import Tuple

import hallucinator as hl


def surface(amplitude: float = 1, frequency: float = 1,
            direction: Tuple[float, float] = (0, 1), phase: float = 0,
            rotate_x: float = 0,
            location: Tuple[int, int, int] = (0, 0, 20),
            camera_pos: Tuple[int, int, int] = (0, 0, 0)):
    resolution = 200
    x_range = (-5, 5)
    y_range = (-5, 5)
    projection_type = 'weak'
    render_density = 10
    surface_func = hl.plane_wave(amplitude, frequency, direction=direction, phase=phase)
    surface_obj = hl.ParaObject3(surface_func,
                                 region_type='2d',
                                 region_params={'a_range': (-3, 3),
                                                'b_range': (-3, 3),
                                                'a_length': 'auto',
                                                'b_length': 'auto'},
                                 species='surface').rotate(theta=rotate_x, axis=(1, 0, 0)).translate(location)
    scene = hl.MonochromeScene()

    scene.add_object(surface_obj, name='surface')
    return hl.camscene(scene, camera_pos,
                       render_density=render_density,
                       projection_type=projection_type,
                       styles='line',
                       x_range=x_range,
                       y_range=y_range,
                       resolution=resolution,)



for i in range(100):
    surface()
