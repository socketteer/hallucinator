import sys

sys.path.append('../hallucinator')
import hallucinator
import math


def at_t(t, scene, backdrop):
    return scene.render_scene(params={'wave': {'t': t}},
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=40,
                              density=20,
                              foreground=hallucinator.WHITE,
                              background=hallucinator.BLACK,
                              display=False,
                              backdrop=backdrop)


scene = hallucinator.MonochromeScene()

path = hallucinator.line(p0=(0, 0), dx=1, dy=0.5)
disturbance = lambda u: 3 / (2 * u ** 2 + 1)

backdrop = hallucinator.MonochromeScene()

backdrop.add_object(hallucinator.axes(x_range=(-10, 10),
                                      y_range=(-10, 10)), "axes")

backdrop_arr = backdrop.render_scene(x_range=(-10, 10),
                                     y_range=(-10, 10),
                                     resolution=40,
                                     density=10,
                                     foreground=hallucinator.WHITE,
                                     background=hallucinator.BLACK)

scene.add_object(hallucinator.disturbance_on_path(disturbance=disturbance,
                                                  v=2,
                                                  init_pos=-10,
                                                  polarization=(-0.5, 1),
                                                  path=path,
                                                  p_range=(-10, 10),
                                                  path_length=math.sqrt(10 ** 2 + 5 ** 2)),
                 name="wave")

hallucinator.video(frame_func=lambda t: at_t(t, scene, backdrop_arr),
                   filename='2d_disturbance_test',
                   t_range=(0, 10),
                   FPS=20)
