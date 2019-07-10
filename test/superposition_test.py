import sys
sys.path.append('../ikonal')
import ikonal
import operator

f = lambda x: 3 / (2 * (x+6) ** 2 + 1)
g = lambda x: -2 / (2 * (x-6) ** 2 + 1)
wf = ikonal.wave(f, 2)
wf2 = ikonal.wave(g, -2)

super = lambda x, t: tuple(map(operator.add, wf(x, t), wf2(x, t)))

ikonal.plot_profile(f=wf,
                    t=0,
                    x_range=(-10, 10),
                    y_range=(-5, 5),
                    density=50)

ikonal.plot_profile(f=wf2,
                    t=0,
                    x_range=(-10, 10),
                    y_range=(-5, 5),
                    density=50)

ikonal.plot_profile(f=super,
                    t=0,
                    x_range=(-10, 10),
                    y_range=(-5, 5),
                    density=50)


ikonal.wave_video(f=super,
                  t_range=(-4, 10),
                  x_range=(-7, 7),
                  y_range=(-5, 5),
                  FPS=10,
                  density=50)
