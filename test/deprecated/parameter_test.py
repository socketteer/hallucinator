import sys

sys.path.append('../hallucinator')
import hallucinator


def at_t(t, scene):
    return scene.render_scene(params={'wave': {'t': t}},
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=40,
                              density=5,
                              foreground=hallucinator.WHITE,
                              background=hallucinator.BLACK,
                              display=False)


scene = hallucinator.MonochromeScene()

scene.add_object(hallucinator.axes(x_range=(-10, 10),
                                   y_range=(-10, 10)), "axes")
f = lambda u: 3 / (2 * u ** 2 + 1)
#TODO this is broken by update on disturbance_on_path
scene.add_object(hallucinator.disturbance_on_path(f=f, v=2, x_range=(-10, 10)), "wave")

hallucinator._deprecated_video(frame_func=lambda t: at_t(t, scene),
                               filename='t_param_test',
                               t_range=(0, 10),
                               FPS=20)
