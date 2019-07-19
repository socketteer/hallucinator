import sys
sys.path.append('../ikonal')
import ikonal
import math

scene = ikonal.MonochromeScene()

scene.add_object(ikonal.vector(p1=(0, 0), p2=(20, 20)), name='vector')

scene.render_scene(x_range=(-40, 40),
                   y_range=(-40, 40),
                   resolution=20,
                   density=2,
                   foreground=ikonal.WHITE,
                   background=ikonal.BLACK,
                   display=True)
