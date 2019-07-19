import sys

sys.path.append('../ikonal')
import ikonal

f = lambda y: 3 / (2 * y ** 2 + 1)
source1 = ikonal.wave_2(f, v=1.5, source=(0, 0), falloff=0.5, starttime=0)

conditions = (lambda x, y: y < x + 5,
              lambda x, y: y > x ** 2 - 4)
cond_region = lambda at, params, density: ikonal.conditional_region(at=at,
                                                                    params=params,
                                                                    conditions=conditions,
                                                                    a_range=(-5, 5),
                                                                    b_range=(-5, 5),
                                                                    density=density)

# TODO think about the fact that translation moves the whole damn thing including conditional region
wave_object = ikonal.ParaObject2(f=source1,
                                 region=cond_region,
                                 species='gradient_wave').translate(tx=3, ty=-2)

scene = ikonal.GrayscaleScene()
scene.add_object(wave_object, "wave")

ikonal.video(frame_func=lambda t: scene.render_scene(params={'wave': {'t': t}},
                                                     x_range=(-5, 5),
                                                     y_range=(-5, 5),
                                                     resolution=20,
                                                     density=10,
                                                     black_ref=0,
                                                     white_ref=3,
                                                     default=ikonal.RED,
                                                     display=False),
             filename='wave_integration_test',
             t_range=(0, 5),
             FPS=10)
