import sys

sys.path.append('../hallucinator')
import hallucinator
import math

scene = hallucinator.MonochromeScene()

spiral = lambda p: (math.cos(p * 2 * math.pi) * math.e ** (-p), math.sin(p * 2 * math.pi) * math.e ** (-p))

scene.add_object(hallucinator.path(path_func=spiral, p_range=(0, 5), path_length=10 * math.pi), name="spiral")

scene.render_scene(x_range=(-2, 2),
                   y_range=(-2, 2),
                   resolution=200,
                   density=10,
                   foreground=hallucinator.WHITE,
                   background=hallucinator.BLACK,
                   display=True)

