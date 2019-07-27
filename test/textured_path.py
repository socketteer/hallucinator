import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math

scene = hl.MonochromeScene()

spiral = lambda p: (math.cos(p * 2 * math.pi) * 10, p * 10, math.sin(p * 2 * math.pi) * 10)

texture = lambda u: math.sin(u * 50)

scene.add_object(hl.textured_path(texture=texture,
                                  pos=-2,
                                  polarization=(0, 1, 0),
                                  path=spiral,
                                  p_range=(-2, 2),
                                  path_length=4 * 2 * 5 * math.pi).translate(tz=60).project("weak", z_factor=0.03),
                 name="wavy_spiral")

scene.render_scene(x_range=(-10, 10),
                   y_range=(-10, 10),
                   resolution=40,
                   density=20,
                   foreground=hl.WHITE,
                   background=hl.BLACK,
                   display=True)
