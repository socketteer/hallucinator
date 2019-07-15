import sys

sys.path.append('../ikonal')
import ikonal
import math
import numpy as np


def rotating_box(t, background):
    speed = 0.5
    frame = ikonal.Scene()
    vector = (math.sin(t), math.cos(t), math.sin(t)*math.cos(t))
    mag = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    normal_vec = (vector[0] / mag, vector[1] / mag, vector[2] / mag)
    frame.add_object(ikonal.box(20, 20, 20, p0=(-10, -10, -10)).rotate(theta=speed * math.pi * t,
                                                                       axis=normal_vec).project(),
                     name="box")

    return ikonal.frame_to_image(frame,
                                 x_range=(-30, 30),
                                 y_range=(-30, 30),
                                 resolution=5,
                                 density=3,
                                 foreground=ikonal.WHITE,
                                 background=ikonal.RED,
                                 backdrop=background)

canvas = ikonal.Scene()

#canvas.add_object(ikonal.axes((-50, 50), (-50, 50), origin=(0, 0)), "axes1")

background = ikonal.frame_to_image(canvas,
                                   x_range=(-30, 30),
                                   y_range=(-30, 30),
                                   resolution=5,
                                   density=1,
                                   foreground=ikonal.WHITE,
                                   background=ikonal.RED)

ikonal.video(frame_func=lambda t: rotating_box(t, background),
             filename='transform_cube_sincos',
             t_range=(0, 20),
             FPS=20)
