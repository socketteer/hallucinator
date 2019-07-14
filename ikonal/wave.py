import numpy as np
import ikonal
import math
import operator


def wave(f, v):
    return lambda x, t: (x, f(x - v * t))


def wave_2(f, v, source=(0, 0), falloff=0, starttime='eternal', defaultval=0):
    func = lambda x, y, t: (x, y, f(math.sqrt((source[0] - x) ** 2 + (source[1] - y) ** 2) - v * t)
                            * np.e ** (-falloff * math.sqrt((source[0] - x) ** 2 + (source[1] - y) ** 2)))
    if starttime == 'eternal':
        return func
    else:
        return lambda x, y, t: (x, y, defaultval) if t < starttime else func(x, y, (t - starttime))


def harmonic(amplitude, wavelength, frequency):
    k = 2 * math.pi / wavelength
    v = frequency * wavelength
    return lambda x, t: (x, amplitude * math.sin(k * (x - v * t)))


def snapshot(f, t, x_range, resolution=1):
    values = []
    for x in np.linspace(x_range[0], x_range[1], x_range[1] - x_range[0] * resolution):
        values.append((x, f(x, t)))
    return values


#does this still work?
def plot_profile(f, t, x_range, y_range, density=1,
                 foreground=ikonal.WHITE, background=ikonal.BLACK,
                 display=True, save=False, filename='profile'):
    plot = profile_scene(f, t, x_range, y_range, density)

    plot.render_scene(x_range=x_range,
                      y_range=y_range,
                      foreground=foreground,
                      background=background,
                      display=display,
                      save=save,
                      filename=filename,
                      resolution=50)


def profile_scene(f, t, x_range, y_range):
    plot = ikonal.Scene()
    plot.add_object(ikonal.axes(x_range, y_range, origin=(0, 0)))
    plot.add_object(ikonal.ParaObject(func=lambda x: f(x, t), path=x_range,
                                      dim=2, species='wave_profile'))
    return plot


def superposition(f1, f2):
    return lambda x, y, t: tuple(map(operator.add, f1(x, y, t), f2(x, y, t)))

