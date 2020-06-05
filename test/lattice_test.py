import sys

sys.path.append('../hallucinator')
import hallucinator
import math
import numpy as np


def rotating_box(t, background):
    speed = 0.2
    frame = hallucinator.MonochromeScene()
    vector = (math.sin(t), math.cos(t), math.sin(t))
    mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    normal_vec = (vector[0] / mag, vector[1] / mag, vector[2] / mag)
    cross = hallucinator.cross(width=10, depth=5, span=20, l_height=40, u_height=20, origin=(-5, -2.5, -30))
    frame.add_object(cross.rotate(theta=math.cos(t) * speed * math.pi * t, axis=normal_vec).project(method='ortho'),
                     name="lattice")

    return frame.render_scene(x_range=(-40, 40),
                              y_range=(-40, 40),
                              resolution=5,
                              density=3,
                              foreground=hallucinator.WHITE,
                              background=hallucinator.RED,
                              backdrop=background,
                              display=False)


canvas = hallucinator.MonochromeScene()

background = canvas.render_scene(x_range=(-40, 40),
                                 y_range=(-40, 40),
                                 resolution=5,
                                 density=1,
                                 foreground=hallucinator.WHITE,
                                 background=hallucinator.RED,
                                 display=False)

hallucinator._deprecated_video(frame_func=lambda t: rotating_box(t, background),
                               filename='latticetest',
                               t_range=(0, 20),
                               FPS=20)
