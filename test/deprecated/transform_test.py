import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math


def scene_at_t(t, background):
    frame = hl.MonochromeScene()
    # hl.render_from_array(background)
    frame.add_object(hl.square(20, p0=(-60, -60)), "nothing")

    frame.add_object(hl.square(20, p0=(-60, -10)).rotate(theta=math.pi * t,
                                                         p=(-50, 0)),
                     "rotate clockwise")

    frame.add_object(hl.square(20, p0=(-60, 40)).rotate(theta=math.pi * -t,
                                                        p=(-50, 50)),
                     "rotate counterclockwise")

    frame.add_object(hl.square(20, p0=(-10, -60)).translate(tx=math.sin(t * math.pi) * 10),
                     "x translate")

    frame.add_object(hl.square(20, p0=(-10, -10)).translate(ty=math.cos(t * math.pi) * 10),
                     "y translate")
    frame.add_object(hl.square(20, p0=(-10, 40)).translate(tx=math.sin(t * math.pi) * 10,
                                                           ty=math.cos(t * math.pi) * 10),
                     "x and y translate")

    '''frame.add_object(hl.square(20, p0=(40, -60)).scale(sx=math.sin(t * math.pi) * 2,
                                                           p=(50, -50)),
                     "x scale")

    frame.add_object(hl.square(20, p0=(40, -10)).scale(sy=math.cos(t * math.pi) * 2,
                                                           p=(50, 0)),
                     "y scale")
    frame.add_object(hl.square(20, p0=(40, 40)).scale(sx=math.sin(t * math.pi) * 2,
                                                          sy=math.cos(t * math.pi) * 2,
                                                          p=(50, 50)),
                     "x and y scale")'''

    frame.add_object(hl.square(20, p0=(40, -60)).shear(sx=math.sin(t * math.pi),
                                                       p=(50, -50)),
                     "x shear")

    frame.add_object(hl.square(20, p0=(40, -10)).shear(sy=math.cos(t * math.pi),
                                                       p=(50, 0)),
                     "y shear")
    frame.add_object(hl.square(20, p0=(40, 40)).shear(sx=math.sin(t * math.pi),
                                                      sy=math.cos(t * math.pi),
                                                      p=(50, 50)),
                     "x and y shear")

    return frame.render_scene(
        x_range=(-80, 80),
        y_range=(-80, 80),
        resolution=5,
        density=2,
        foreground=hl.WHITE,
        background=hl.BLACK,
        backdrop=background)


canvas = hl.MonochromeScene()
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(-50, 0)), "axes1")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(-50, 50)), "axes2")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(-50, -50)), "axes3")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(0, 0)), "axes4")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(0, 50)), "axes5")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(0, -50)), "axes6")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(50, 0)), "axes7")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(50, 50)), "axes8")
canvas.add_object(hl.axes((-20, 20), (-20, 20), origin=(50, -50)), "axes9")

background = canvas.render_scene(x_range=(-80, 80),
                                 y_range=(-80, 80),
                                 resolution=5,
                                 density=2,
                                 foreground=hl.WHITE,
                                 background=hl.RED)

hl._deprecated_video(frame_func=lambda t: scene_at_t(t, background),
                     filename='transform_test_6',
                     t_range=(0, 10),
                     FPS=20)
