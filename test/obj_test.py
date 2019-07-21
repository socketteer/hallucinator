import sys
sys.path.append('../hallucinator')
import hallucinator
import math

scene = hallucinator.MonochromeScene()

scene.add_object(hallucinator.vector(p1=(0, 0), p2=(20, 20)), name='vector')

scene.render_scene(x_range=(-40, 40),
                   y_range=(-40, 40),
                   resolution=20,
                   density=2,
                   foreground=hallucinator.WHITE,
                   background=hallucinator.BLACK,
                   display=True)
