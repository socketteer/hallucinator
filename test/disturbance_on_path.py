import sys

sys.path.append('../hallucinator')
import hallucinator as hal
import math


def at_t(t, scene, backdrop):
    return scene.render_scene(params={'wave': {'t': t}},
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=40,
                              density=20,
                              foreground=hal.WHITE,
                              background=hal.BLACK,
                              display=False,
                              backdrop=backdrop)


scene = hal.MonochromeScene()

path = hal.line_parametric(p0=(0, 0), dx=1, dy=0.5)
f = lambda u: 3 / (2 * u ** 2 + 1)
disturbance = hal.propagating_disturbance(f, v=2)

backdrop = hal.MonochromeScene()

backdrop.add_object(hal.axes(x_range=(-10, 10),
                             y_range=(-10, 10)), "axes")

backdrop_arr = backdrop.render_scene(x_range=(-10, 10),
                                     y_range=(-10, 10),
                                     resolution=40,
                                     density=10,
                                     foreground=hal.WHITE,
                                     background=hal.BLACK)

scene.add_object(hal.disturbance_on_path(disturbance=disturbance,
                                         polarization=(-0.5, 1),
                                         init_pos=-10,
                                         path=path,
                                         p_range=(-10, 10),
                                         path_length=math.sqrt(10 ** 2 + 5 ** 2)),
                 name="wave")

hal.video(frame_func=lambda t: at_t(t, scene, backdrop_arr),
          filename='2d_disturbance_test',
          t_range=(0, 10),
          FPS=20)
