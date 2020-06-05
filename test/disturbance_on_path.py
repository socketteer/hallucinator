import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math


def at_t(t, scene, backdrop):
    return scene.render_scene(params={'wave': {'t': t}},
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=40,
                              density=20,
                              foreground=hl.WHITE,
                              background=hl.BLACK,
                              display=False,
                              backdrop=backdrop)


scene = hl.MonochromeScene()

path = hl.line_parametric(p0=(0, 0), dx=1, dy=0.5)
f = lambda u: 3 / (2 * u ** 2 + 1)
disturbance = hl.propagating_disturbance(f, v=2)

backdrop = hl.MonochromeScene()

backdrop.add_object(hl.axes(x_range=(-10, 10),
                            y_range=(-10, 10)), "axes")

backdrop_arr = backdrop.render_scene(x_range=(-10, 10),
                                     y_range=(-10, 10),
                                     resolution=40,
                                     density=10,
                                     foreground=hl.WHITE,
                                     background=hl.BLACK)

# TODO fix this
scene.add_object(hl.disturbance_on_path(disturbance=disturbance,
                                        polarization=(-0.5, 1),
                                        init_pos=-10,
                                        path=path,
                                        p_range=(-10, 10),
                                        path_length=math.sqrt(10 ** 2 + 5 ** 2)),
                 name="wave")

hl._deprecated_video(frame_func=lambda t: at_t(t, scene, backdrop_arr),
                     filename='2d_disturbance_test',
                     t_range=(0, 10),
                     FPS=20)
