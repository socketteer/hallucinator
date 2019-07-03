import numpy as np
import obj
import scene
import group
import render


def wave(f, v):
    return lambda x, t: f(x - v * t)


def snapshot(f, t, x_range, resolution=1):
    values = []
    for x in np.linspace(x_range[0], x_range[1], x_range[1] - x_range[0] * resolution):
        values.append((x, f(x, t)))
    return values


def plot_profile(f, t, x_range, y_range, density=1,
                 foreground=render.WHITE, background=render.BLACK,
                 display=True, save=False, filename='profile'):
    plot = scene.Scene()
    plot.add_object(obj.axes(x_range, y_range, origin=(0, 0)))
    plot.add_object(group.ParaObject(func=lambda x: f(x, t), path=x_range,
                                     num_points=x_range[1] - x_range[0] * density,
                                     dim=2, species='wave_profile'))
    # if y_range == 'default': pass

    plot.discr_render(x_range=x_range,
                      y_range=y_range,
                      foreground=foreground,
                      background=background,
                      display=display,
                      save=save,
                      filename=filename,
                      resolution=50)


def generate_video(f, t_range, x_range, y_range, density=1,
                   foreground=render.WHITE, background=render.BLACK,
                   display=True, save=False, filename='wavefunction'):
    pass
