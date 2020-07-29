import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math


def gen_spiral(location=(0, 0, 20), coil_density=1, radius=1, turns=5, rotate_x=math.pi/4, camera_pos=(0, 0, 0),
               render_density=100,
               projection_type='weak',
               x_range=(-3, 3),
               y_range=(-3, 3),
               resolution=200):
    scene = hl.MonochromeScene()

    spiral = lambda p: (math.cos(p * 2 * math.pi)*radius - location[0],
                        p/coil_density - location[1],
                        math.sin(p * 2 * math.pi)*radius - location[2])

    spiral_obj = scene.add_object(hl.path_3(path_func=spiral,
                                            p_range=(0, turns),
                                            path_length=10 * math.pi).rotate(theta=rotate_x,
                                                                             axis=(1, 0, 0),
                                                                             p=location),
                                  name="coil")

    return hl.camscene(scene, camera_pos,
                       render_density=render_density,
                       projection_type=projection_type,
                       x_range=x_range,
                       y_range=y_range,
                       resolution=resolution)


hl.render_from_array(gen_spiral(location=(0, 0, 20),
                                coil_density=5,
                                radius=1,
                                turns=10,
                                rotate_x=0,
                                camera_pos=(0, 0, -20),
                                render_density=100,
                                projection_type='weak',
                                x_range=(-5, 5),
                                y_range=(-5, 5),
                                resolution=200))
