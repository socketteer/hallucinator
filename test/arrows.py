import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math

scene = hl.MonochromeScene()

scene.add_object(hl.arrow(p0=(0, 0), direction=(1, 0), length=1, head_length=0.3), name="arrow1")
scene.add_object(hl.arrow(p0=(1, 1), direction=(0, 1), length=1, head_length=0.3), name="arrow2")
scene.add_object(hl.arrow(p0=(-3, -3), direction=(1, 5), length=3, head_length=0.3), name="arrow3")


scene.render_scene(x_range=(-10, 10),
                   y_range=(-10, 10),
                   resolution=50,
                   density=20,
                   display=True)
