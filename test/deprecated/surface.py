import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math

scene = hl.MonochromeScene()

f = lambda a, b: (a, 0.2 * math.sin(a * math.pi) ** 2 + 0.2 * math.sin(b * math.pi) + 0.5 / (abs(a) + abs(b)), b)

scene.add_object(hl.surface(surface_func=f,
                            a_range=(-5, 5),
                            b_range=(-5, 5)).rotate(theta=-math.pi / 8,
                                                    axis=(1, 0, 0)).rotate(math.pi/8, (0, 1, 0)).translate(tz=25).project("weak"),
                 name="cursedlasagna")

scene.add_object(hl.axes_3((-6, 6), (-6, 6), (-6, 6)).rotate(theta=-math.pi / 8,
                                                    axis=(1, 0, 0)).rotate(math.pi/8, (0, 1, 0)).translate(tz=25).project("weak"),
                 name='axes')

scene.render_scene(x_range=(-6, 6),
                   y_range=(-6, 6),
                   resolution=150,
                   density=50,
                   display=True,
                   background=hl.BLUE)
