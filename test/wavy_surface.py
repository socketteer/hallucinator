import hallucinator as hl
from typing import TypedDict, NamedTuple, Tuple
import math


def wavy_surface(amplitude: float = 1,
                 frequency: float = 1,
                 direction: float = 0,
                 phase: float = 0,
                 rotate_x: float = 0,
                 rotate_y: float = 0,
                 rotate_z: float = 0,
                 location: Tuple[int, int, int] = (0, 0, 20)):

    surface_obj = hl.ParaObject3(hl.gen_plane_wave(amplitude, frequency, hl.unit_vector(direction), phase),
                                 region_type='2d',
                                 region_params={'surface_range': ((-5, 5), (-5, 5))},
                                 species='surface')
    surface_obj = surface_obj.rotate(theta=rotate_x, axis=(1, 0, 0))
    surface_obj = surface_obj.rotate(theta=rotate_y, axis=(0, 1, 0))
    surface_obj = surface_obj.rotate(theta=rotate_z, axis=(0, 0, 1))
    surface_obj = surface_obj.translate(location)
    return surface_obj


def wavy_scene(t, **kwargs):
    scene = hl.MonochromeScene()
    scene.add_object(wavy_surface(amplitude=1,
                                  frequency=t,
                                  direction=0,
                                  phase=0,
                                  rotate_x=-1,
                                  rotate_y=4,
                                  rotate_z=1,
                                  location=(0, 0, 40)),
                     "surface")

    camscene = scene.render_scene(camera_position=(0, 0, -15),
                                  projection_type=hl.Projections.WEAK,
                                  styles=hl.Styles.UNIFORM,
                                  x_range=(-7, 7),
                                  y_range=(-7, 7),
                                  resolution=75,
                                  densities=(6, 30))

    return camscene


#hl.render_from_array(wavy_scene(t=0))


params = dict(
        frame_function=lambda d: wavy_scene(**d),
        frame_arguments=hl.unroll_dict(dict(
            t=hl.np.linspace(0, 37, num=1500),
        )),
        filename=f"../videos/lasagna3",
        fps=15,
        preview=True,
        parallel_frames=False,
    )

hl.video(**params)
