import sys

import math

sys.path.append('../hallucinator')
import hallucinator as hl


def rotating_wheel(t, frequency):
    canvas = hl.MonochromeScene()
    canvas.add_object(hl.wheel(radius=1, num_spokes=10).rotate(theta=math.pi * 2 * frequency * t), "wheel")

    return canvas.render_scene(x_range=(-2, 2),
                               y_range=(-2, 2),
                               resolution=200,
                               density=30,
                               foreground=hl.WHITE,
                               background=hl.BLACK,
                               display=False)


frequency = 2.3

hl._deprecated_video(frame_func=lambda t: rotating_wheel(t, frequency),
                     filename='rotating_wheel_frequency_{0}'.format(frequency),
                     t_range=(0, 1),
                     FPS=20)