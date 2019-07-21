import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math

scene = hl.MonochromeScene()

spiral = lambda p: (math.cos(p * 2 * math.pi), p / 3, math.sin(p * 2 * math.pi) + 20)

scene.add_object(hl.path_3(path_func=spiral,
                           p_range=(-5, 5),
                           path_length=10 * math.pi).rotate(theta=math.pi / 4,
                                                            axis=(1, 0, 0),
                                                            p=(0, 0, 20)).project("weak"),
                 name="coil")

scene.render_scene(x_range=(-2, 2),
                   y_range=(-3, 3),
                   resolution=200,
                   density=50,
                   foreground=hl.WHITE,
                   background=hl.BLACK,
                   display=True)
