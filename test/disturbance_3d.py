import sys

sys.path.append('../hallucinator')
import hallucinator
import math


def at_t(t, scene, backdrop):
    return scene.render_scene(params={'wave': {'t': t}},
                              x_range=(-20, 20),
                              y_range=(-20, 20),
                              resolution=20,
                              density=10,
                              foreground=hallucinator.WHITE,
                              background=hallucinator.RED,
                              display=False,
                              backdrop=backdrop)


scene = hallucinator.MonochromeScene()

spiral = lambda p: (math.cos(p * 2 * math.pi) * 10, p * 10, math.sin(p * 2 * math.pi) * 10)

disturbance = lambda u: 3 / (2 * u ** 2 + 1)
#disturbance = lambda u: math.sin(u*50)

backdrop = hallucinator.MonochromeScene()

backdrop.add_object(hallucinator.axes(x_range=(-20, 20),
                                      y_range=(-20, 20)), "axes")

backdrop_arr = backdrop.render_scene(x_range=(-20, 20),
                                     y_range=(-20, 20),
                                     resolution=20,
                                     density=5,
                                     foreground=hallucinator.WHITE,
                                     background=hallucinator.RED)

scene.add_object(hallucinator.disturbance_on_path_3(disturbance=disturbance,
                                                    v=2,
                                                    init_pos=-2,
                                                    polarization=(0, 1, 0),
                                                    path=spiral,
                                                    p_range=(-2, 2),
                                                    path_length=4 * 2 * 5 * math.pi).translate(tz=50).project("weak", z_factor=0.03),
                 name="wave")

hallucinator.video(frame_func=lambda t: at_t(t, scene, backdrop_arr),
                   filename='3d_smooth_disturbance_test',
                   t_range=(0, 5),
                   FPS=20)
