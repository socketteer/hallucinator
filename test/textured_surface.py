import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math

scene = hl.MonochromeScene()
texture = lambda u: 2 * -math.sin(u * math.pi) / u

scene.add_object(hl.textured_surface(texture=texture,
                                     pos=(0, 0),
                                     polarization=(-1, 0, 0),
                                     surface=hl.plane(p0=(0, 0, 0),
                                                      v1=(0, 1, 0),
                                                      v2=(0, 0, 1)),
                                     a_range=(-15, 15),
                                     b_range=(-15, 15)).rotate(theta=math.pi / 8,
                                                               axis=(0, 1, 0)).translate(
    tz=30).project("weak"),
                 name='basin')

scene.render_scene(x_range=(-20, 20),
                   y_range=(-20, 20),
                   resolution=50,
                   style='line',
                   region_params={'a_spacing': 0.5,
                                  'b_spacing': 0.5},
                   foreground=hl.BLUE,
                   background=hl.BLACK,
                   display=True)
