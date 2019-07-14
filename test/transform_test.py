import sys

sys.path.append('../ikonal')
import ikonal
import math


def scene_at_t(t, background):
    frame = ikonal.Scene()
    # ikonal.render_from_array(background)
    frame.add_object(ikonal.square(20, p0=(-60, -60)), "nothing")

    frame.add_object(ikonal.square(20, p0=(-60, -10)).rotate(theta=math.pi * t,
                                                             p=(-50, 0)),
                     "rotate clockwise")

    frame.add_object(ikonal.square(20, p0=(-60, 40)).rotate(theta=math.pi * -t,
                                                            p=(-50, 50)),
                     "rotate counterclockwise")

    frame.add_object(ikonal.square(20, p0=(-10, -60)).translate(x=math.sin(t * math.pi) * 10),
                     "x translate")

    frame.add_object(ikonal.square(20, p0=(-10, -10)).translate(y=math.sin(t * math.pi) * 10),
                     "y translate")
    frame.add_object(ikonal.square(20, p0=(-10, 40)).translate(x=math.sin(t * math.pi) * 10,
                                                               y=math.cos(t * math.pi) * 10),
                     "x and y translate")

    frame.add_object(ikonal.square(20, p0=(40, -60)).scale(x=math.sin(t * math.pi) * 2,
                                                           p=(50, -50)),
                     "x scale")

    frame.add_object(ikonal.square(20, p0=(40, -10)).scale(y=math.sin(t * math.pi) * 2,
                                                           p=(50, 0)),
                     "y scale")
    frame.add_object(ikonal.square(20, p0=(40, 40)).scale(x=math.sin(t * math.pi) * 2,
                                                          y=math.cos(t * math.pi) * 2,
                                                          p=(50, 50)),
                     "x and y scale"),

    return ikonal.frame_to_image(frame,
                                 x_range=(-80, 80),
                                 y_range=(-80, 80),
                                 resolution=10,
                                 density=2,
                                 foreground=ikonal.WHITE,
                                 background=ikonal.BLACK,
                                 backdrop=background)


canvas = ikonal.Scene()
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(-50, 0)), "axes1")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(-50, 50)), "axes2")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(-50, -50)), "axes3")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(0, 0)), "axes4")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(0, 50)), "axes5")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(0, -50)), "axes6")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(50, 0)), "axes7")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(50, 50)), "axes8")
canvas.add_object(ikonal.axes((-20, 20), (-20, 20), origin=(50, -50)), "axes9")

background = ikonal.frame_to_image(canvas,
                                   x_range=(-80, 80),
                                   y_range=(-80, 80),
                                   resolution=10,
                                   density=2,
                                   foreground=ikonal.WHITE,
                                   background=ikonal.BLACK)

ikonal.video(frame_func=lambda t: scene_at_t(t, background),
             filename='transform_test',
             t_range=(0, 10),
             FPS=20)
