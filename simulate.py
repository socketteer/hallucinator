import discretizer
import render
import scene
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
def generate_video(frame, transition_rule,
                   filename, width=2000, height=2000,
                   x_range=(-1000, 1000), y_range=(-1000, 1000),
                   foreground=render.WHITE, background=render.BLACK,
                   FPS=5, seconds=5):
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(FPS), (width, height))

    for _ in range(FPS * seconds):
        video.write(scene.frame_to_image(frame,
                                         x_range=x_range, y_range=y_range,
                                         foreground=foreground, background=background))
        frame = transition_rule(frame)

    video.release()


def generate_video_3(frame, transition_rule,
                     filename, width=2000, height=2000,
                     x_range=(-1000, 1000), y_range=(-1000, 1000),
                     pov=(0, 0, 0), z_scale=0.005,
                     foreground=render.WHITE, background=render.BLACK,
                     FPS=5, seconds=5):
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(FPS), (width, height))

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
