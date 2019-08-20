import numpy as np
import hallucinator
import math
import operator


def propagating_disturbance(f, v):
    return lambda p, t: (p, f(p - v * t))


def harmonic(amplitude, wavelength, frequency):
    k = 2 * math.pi / wavelength
    v = frequency * wavelength
    return lambda p, t: (p, amplitude * math.sin(k * (p - v * t)))


def wave_2(f, v, source=(0, 0), falloff=0, starttime='eternal', defaultval=0):
    func = lambda a, b, t: (a, b, f(math.sqrt((source[0] - a) ** 2 + (source[1] - b) ** 2) - v * t)
                            * np.e ** (-falloff * math.sqrt((source[0] - a) ** 2 + (source[1] - b) ** 2)))
    if starttime == 'eternal':
        return func
    else:
        return lambda a, b, t: (a, b, defaultval) if t < starttime else func(a, b, (t - starttime))


def superposition(f1, f2):
    return lambda x, y, t: tuple(map(operator.add, f1(x, y, t), f2(x, y, t)))




'''def snapshot(f, t, x_range, resolution=1):
    values = []
    for x in np.linspace(x_range[0], x_range[1], x_range[1] - x_range[0] * resolution):
        values.append((x, f(x, t)))
    return values'''


#does this still work?
'''def plot_profile(f, t, x_range, y_range, density=1,
                 foreground=hallucinator.WHITE, background=hallucinator.BLACK,
                 display=True, save=False, filename='profile'):
    plot = profile_scene(f, t, x_range, y_range, density)

    plot.render_scene(x_range=x_range,
                      y_range=y_range,
                      foreground=foreground,
                      background=background,
                      display=display,
                      save=save,
                      filename=filename,
                      resolution=50)'''


'''def profile_scene(f, t, x_range, y_range):
    plot = hallucinator.Scene()
    plot.add_object(hallucinator.axes(x_range, y_range, origin=(0, 0)))
    plot.add_object(hallucinator.ParaObject(func=lambda x: f(x, t), path=x_range,
                                            dim=2, species='wave_profile'))
    return plot'''


