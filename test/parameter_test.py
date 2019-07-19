import sys

sys.path.append('../ikonal')
import ikonal


def at_t(t, scene):
    return scene.render_scene(params={'wave': {'t': t}},
                              x_range=(-10, 10),
                              y_range=(-10, 10),
                              resolution=40,
                              density=5,
                              foreground=ikonal.WHITE,
                              background=ikonal.BLACK,
                              display=False)


scene = ikonal.MonochromeScene()

scene.add_object(ikonal.axes(x_range=(-10, 10),
                             y_range=(-10, 10)), "axes")
f = lambda u: 3 / (2 * u ** 2 + 1)
scene.add_object(ikonal.wave_primitive(f=f, v=2, x_range=(-10, 10)), "wave")

ikonal.video(frame_func=lambda t: at_t(t, scene),
             filename='t_param_test',
             t_range=(0, 10),
             FPS=20)
