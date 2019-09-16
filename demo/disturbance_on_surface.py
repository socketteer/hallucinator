import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math

scene = hl.MonochromeScene()
disturbance = lambda u: 0.5 * math.sin(u * math.pi)

scene.add_object(hl.disturbance_on_surface(disturbance=disturbance,
                                           v=2,
                                           init_pos=(0, 0),
                                           polarization=(-1, 0, 0),
                                           surface=hl.plane(p0=(0, 0, 0),
                                                            v1=(0, 1, 0),
                                                            v2=(0, 0, 1)),
                                           a_range=(-15, 15),
                                           b_range=(-15, 15)).rotate(theta=-math.pi / 4,
                                                                     axis=(1, 0, 0)).rotate(math.pi / 8,
                                                                                            (0, 1, 0)).translate(
    tz=40).project("weak"),
                 name='basin')

hl.video(frame_func=lambda t: scene.render_scene(params={'basin': {'t': t}},
                                                 x_range=(-20, 20),
                                                 y_range=(-20, 20),
                                                 resolution=50,
                                                 style='line',
                                                 region_params={'a_spacing': 0.3,
                                                                'b_spacing': 0.3},
                                                 foreground=hl.WHITE,
                                                 background=hl.BLACK,
                                                 display=False),
         filename='disturbance_on_surface_wireframe',
         t_range=(0, 5),
         FPS=15)
