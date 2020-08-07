import hallucinator as hl
import math

scene = hl.MonochromeScene()

location = (5, -10, 40)
location_2 = (0, 8, 60)
spiral_location = (-7, -10, 10)
rotate_x = math.pi / 4
scene.add_object(hl.ParaObject3(hl.gen_ripple(amplitude=0.5, frequency=3, phase=0),
                                region_type='2d',
                                region_params={'surface_range': ((-10, 10), (-10, 10))},
                                species='surface').rotate(theta=rotate_x, axis=(1, 0, 0)).translate(location),
                 "ripple")
scene.add_object(hl.ParaObject3(hl.gen_ripple(amplitude=0.5, frequency=3, phase=0),
                                region_type='2d',
                                region_params={'surface_range': ((-10, 10), (-10, 10))},
                                species='surface').rotate(theta=-rotate_x, axis=(1, 1, 0)).translate(location_2),
                 "ripple2")

scene.add_object(hl.path_3(path_func=hl.gen_spiral(coil_density=1, radius=2),
                           p_range=(0, 10),
                           path_length=10 * math.pi).translate(spiral_location),
                 "spiral")

camscene = scene.render_scene(camera_position=(0, -3, -50),
                              projection_type=hl.Projections.WEAK,
                              styles={'ripple': hl.Styles.WIREFRAME,
                                      'ripple2': hl.Styles.UNIFORM,
                                      'spiral': hl.Styles.UNIFORM},
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=50,
                              densities={'ripple': (3, 3),
                                         'ripple2': (5, 5),
                                         'spiral': 50})

hl.render_from_array(camscene)
