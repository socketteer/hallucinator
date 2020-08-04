import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np


def rotating_box(t, background):
    frame = hl.MonochromeScene()

    for i in range(3):
        frame.add_object(hl.box(30, 30, 30, (-50 + 50 * i, 25, 30)), "box{0}".format(i))

    for i in range(3):
        frame.add_object(hl.box(30, 30, 30, (-50 + 50 * i, -40, 30)), "box{0}".format(i+3))

    frame.objects["box0"] = frame.objects["box0"].shear(xy=math.sin(t), p=(-50, 25, 30))
    frame.objects["box1"] = frame.objects["box1"].shear(xz=math.sin(t), p=(0, 25, 30))
    frame.objects["box2"] = frame.objects["box2"].shear(yx=math.sin(t), p=(50, 25, 30))
    frame.objects["box3"] = frame.objects["box3"].shear(yz=math.sin(t), p=(-50, -40, 30))
    frame.objects["box4"] = frame.objects["box4"].shear(zx=math.sin(t), p=(0, -40, 30))
    frame.objects["box5"] = frame.objects["box5"].shear(zy=math.sin(t), p=(50, -40, 30))

    for i in range(3):
        frame.objects["box{0}".format(i)] = frame.objects["box{0}".format(i)].rotate(math.pi / 8,
                                                                                     (1, 0, 0),
                                                                                     (-50 + -50 * i, 25, 30))
        frame.objects["box{0}".format(i)] = frame.objects["box{0}".format(i)].project("ortho")

    for i in range(3, 6):
        frame.objects["box{0}".format(i)] = frame.objects["box{0}".format(i)].rotate(math.pi / 8,
                                                                                     (1, 0, 0),
                                                                                     (-50 + -50 * i, -40, 30))
        frame.objects["box{0}".format(i)] = frame.objects["box{0}".format(i)].project("ortho")

    return frame.render_scene(x_range=(-100, 100),
                              y_range=(-100, 100),
                              resolution=5,
                              density=3,
                              foreground=hl.WHITE,
                              background=hl.RED,
                              backdrop=background,
                              display=False)


canvas = hl.MonochromeScene()

# canvas.add_object(hallucinator.axes((-50, 50), (-50, 50), origin=(0, 0)), "axes1")

background = canvas.render_scene(x_range=(-100, 100),
                                 y_range=(-100, 100),
                                 resolution=5,
                                 density=1,
                                 foreground=hl.WHITE,
                                 background=hl.RED,
                                 display=False)

hl._deprecated_video(frame_func=lambda t: rotating_box(t, background),
                     filename='cube_shear_test',
                     t_range=(0, 5),
                     FPS=20)

