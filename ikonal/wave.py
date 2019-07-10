import numpy as np
import ikonal
import math


def wave(f, v):
    return lambda x, t: (x, f(x - v * t))


def wave_2(f, v, source=(0, 0), falloff=0):
    return lambda x, y, t: (x, y, f(math.sqrt((source[0] - x) ** 2 + (source[1] - y) ** 2) - v * t)
                            * np.e ** (-falloff * math.sqrt((source[0] - x) ** 2 + (source[1] - y) ** 2)))


def harmonic(amplitude, wavelength, frequency):
    k = 2 * math.pi / wavelength
    v = frequency * wavelength
    return lambda x, t: (x, amplitude * math.sin(k * (x - v * t)))


def snapshot(f, t, x_range, resolution=1):
    values = []
    for x in np.linspace(x_range[0], x_range[1], x_range[1] - x_range[0] * resolution):
        values.append((x, f(x, t)))
    return values


def plot_profile(f, t, x_range, y_range, density=1,
                 foreground=ikonal.WHITE, background=ikonal.BLACK,
                 display=True, save=False, filename='profile'):
    plot = profile_scene(f, t, x_range, y_range, density)

    plot.discr_render(x_range=x_range,
                      y_range=y_range,
                      foreground=foreground,
                      background=background,
                      display=display,
                      save=save,
                      filename=filename,
                      resolution=50)


# this is more general?
def wave_video(f, t_range, x_range, y_range, density=1, resolution=50,
               foreground=ikonal.WHITE, background=ikonal.BLACK,
               FPS=5, filename='wavefunction'):
    ikonal.generate_video_t(f=lambda t: profile_scene(f, t, x_range, y_range, density),
                            filename=filename,
                            t_range=t_range,
                            x_range=x_range,
                            y_range=y_range,
                            resolution=resolution,
                            foreground=foreground,
                            background=background,
                            FPS=FPS)


def wave_2_gradient_video(f, t_range, x_range, y_range, resolution=50,
                          white_ref=-1.0, black_ref=1.0,
                          fps=5, filename='wavefunction'):
    ikonal.video(frame_func=lambda t: ikonal.gradient_frame(f, t, x_range=x_range,
                                                            y_range=y_range,
                                                            white_ref=white_ref,
                                                            black_ref=black_ref,
                                                            resolution=resolution),
                 filename=filename,
                 t_range=t_range,
                 FPS=fps)


def gradient_frame(f, t, x_range, y_range, white_ref=-1.0, black_ref=1.0, resolution=50):
    phasegrid = ikonal.phasegrid(lambda x, y: f(x, y, t)[2],
                                 x_range=x_range,
                                 y_range=y_range,
                                 resolution=resolution)
    grad = ikonal.arr_to_gradient(phasegrid,
                                  white_ref=white_ref,
                                  black_ref=black_ref)
    return grad


def profile_scene(f, t, x_range, y_range, density=1):
    plot = ikonal.Scene()
    plot.add_object(ikonal.axes(x_range, y_range, origin=(0, 0)))
    plot.add_object(ikonal.ParaObject(func=lambda x: f(x, t), path=x_range,
                                      num_points=x_range[1] - x_range[0] * density,
                                      dim=2, species='wave_profile'))
    return plot
