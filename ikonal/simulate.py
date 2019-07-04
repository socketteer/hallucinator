import ikonal
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

'''
def simulate(init, rule, steps):
    """

    :param init:
    :param rule:
    :param steps:
    :return:
    """
    spacetime = []
    spacetime.append(init)
    for step in range(steps):
        init = rule(init)
        spacetime.append(init)
    return spacetime
'''

#TODO make these methods of scene?
#TODO resolution, etc
def generate_video(frame, transition_rule,
                   filename, width=2000, height=2000,
                   x_range=(-1000, 1000), y_range=(-1000, 1000),
                   foreground=ikonal.WHITE, background=ikonal.BLACK,
                   FPS=5, seconds=5):
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(FPS), (width, height))

    for _ in range(FPS * seconds):
        video.write(ikonal.frame_to_image(frame,
                                         x_range=x_range, y_range=y_range,
                                         foreground=foreground, background=background))
        frame = transition_rule(frame)

    video.release()


def generate_video_t(f, filename, t_range=(0, 10), x_range=(-10, 10), y_range=(-10, 10), resolution=50,
                   foreground=ikonal.WHITE, background=ikonal.BLACK,
                   FPS=5):
    """

    :param frame:
    :param f:
    :param filename:
    :param width:
    :param height:
    :param x_range:
    :param y_range:
    :param resolution:
    :param foreground:
    :param background:
    :param FPS:
    :param seconds:
    :return:
    generate frames with time parameters
    """
    fourcc = VideoWriter_fourcc(*'MP42')
    height = (y_range[1] - y_range[0]) * resolution
    width = (x_range[1] - x_range[0]) * resolution
    height = int(height)
    width = int(width)
    video = VideoWriter('./videos/{0}.avi'.format(filename),
                        fourcc, FPS, frameSize=(height, width))

    interval = t_range[1] - t_range[0]
    time = t_range[0]
    for _ in range(np.rint(FPS * interval).astype(int)):
        frame = f(time)
        video.write(ikonal.frame_to_image(frame,
                                          x_range=x_range,
                                          y_range=y_range,
                                          foreground=foreground,
                                          background=background,
                                          resolution=resolution))
        time += 1/FPS


    video.release()


def generate_video_3(frame, transition_rule,
                     filename, width=2000, height=2000,
                     x_range=(-1000, 1000), y_range=(-1000, 1000),
                     pov=(0, 0, 0), z_scale=0.005,
                     foreground=ikonal.WHITE, background=ikonal.BLACK,
                     FPS=5, seconds=5):
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(FPS), (height, width))

    for _ in range(FPS * seconds):
        video.write(frame.lazy_render(x_range=x_range,
                                      y_range=y_range,
                                      pov=pov,
                                      z_scale=z_scale,
                                      foreground=foreground,
                                      background=background,
                                      display=False, save=False))
        frame = transition_rule(frame)

    video.release()
