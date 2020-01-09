import collections
from multiprocessing.pool import Pool
from pprint import pprint

import cv2
import numpy as np
from PIL import Image
from bresenham import bresenham

from hallucinator.utility import set_global_function, call_global_function
import hallucinator as hl
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (127, 127, 127)


def canvas(w, h, color=BLACK):
    canv = np.full((w, h, 3), color, dtype=np.uint8)
    return canv


def line(x0, x1, y0, y1):
    return list(bresenham(x0, x1, y0, y1))


def render_from_array(data):
    img = Image.fromarray(np.rot90(data))
    img.show()


def save_img(data, filename):
    img = Image.fromarray(np.rot90(data))
    img.save('./images/{0}.jpg'.format(filename))


# TODO test existing canvas
def set_to_bichrome(points, x_range, y_range, foreground=WHITE, background=BLACK, resolution=5, backdrop="new"):
    """
    :param points: set of points (x, y) to draw in foreground color
    :param x_range: range (xi, xf) of coordinates to render
    :param y_range: range (yi, yf) of coordinates to render
    :param foreground: foreground color (R, G, B)
    :param background: background color (R, G, B)
    :param resolution: pixels per unit of x and y
    :param canv: optional existing canvas to write over
    :return:
    """
    if backdrop == "new":
        canv = np.full(((x_range[1] - x_range[0]) * resolution,
                        (y_range[1] - y_range[0]) * resolution,
                        3),
                       background, dtype=np.uint8)
    else:
        canv = backdrop.copy()
    for p in points:
        x = p[0]
        y = p[1]
        if x_range[0] <= x < x_range[1] - (1 / resolution) and y_range[0] <= y < y_range[1] - (1 / resolution):
            x_addr = np.rint((x - x_range[0]) * resolution).astype(int)
            y_addr = np.rint((y - y_range[0]) * resolution).astype(int)
            canv[x_addr, y_addr] = foreground
    return canv


def lines_to_bichrome(lines, x_range, y_range, foreground=WHITE, background=BLACK, resolution=5, backdrop="new"):
    if backdrop == "new":
        canv = np.full(((x_range[1] - x_range[0]) * resolution,
                        (y_range[1] - y_range[0]) * resolution,
                        3),
                       background, dtype=np.uint8)
    else:
        canv = backdrop.copy()
    for l in lines:
        if x_range[0] <= l[0][1] < x_range[1] - (1 / resolution) \
                and y_range[0] <= l[1][1] < y_range[1] - (1 / resolution):
            x_pix_1 = np.rint((l[0][0] - x_range[0]) * resolution).astype(int)
            x_pix_2 = np.rint((l[0][1] - x_range[0]) * resolution).astype(int)
            y_pix_1 = np.rint((l[1][0] - y_range[0]) * resolution).astype(int)
            y_pix_2 = np.rint((l[1][1] - x_range[0]) * resolution).astype(int)
            for point in line(x_pix_1, x_pix_2, y_pix_1, y_pix_2):
                try:
                    canv[point[0], point[1]] = foreground
                except IndexError:
                    # print('index error')
                    pass
    return canv


# test for weird things like black and white switched
def arr_to_gradient(arr, black_ref=-1.0, white_ref=1.0):
    """
    :param arr:
    :param black_ref:
    :param white_ref:
    :return:
    """
    canv = np.empty((arr.shape[0], arr.shape[1], 3), dtype=np.uint8)
    A = (white_ref - black_ref) / 2
    d = (white_ref + black_ref) / 2

    for x in range(np.shape(arr)[0]):
        for y in range(np.shape(arr)[1]):
            gradient = (arr[x][y] - d) / A
            gradient = np.rint(255 * (gradient + 1) / 2).astype(int)
            canv[x][y] = (gradient, gradient, gradient)

    return canv


# TODO make methods from reused functionality
# TODO need range-1 here too for rounding?
# TODO Make parallel
def set_to_gradient(points, x_range, y_range, black_ref=-1.0, white_ref=1.0, default=BLUE, resolution=5,
                    backdrop="new"):
    """
    :param points: set of points (x, y, gradient)
    :param x_range: range (xi, xf) of coordinates to render
    :param y_range: range (yi, yf) of coordinates to render
    :param black_ref: reference value for black
    :param white_ref: reference value for white
    :param default: color of pixels not in points
    :param resolution: pixels per unit of x and y
    :param canv: optional existing canvas to write over
    :return: array of (gradient, gradient, gradient)
    """
    A = (white_ref - black_ref) / 2
    d = (white_ref + black_ref) / 2
    x_pixels = math.ceil((x_range[1] - x_range[0]) * resolution)
    y_pixels = math.ceil((y_range[1] - y_range[0]) * resolution)
    if backdrop == "new":
        canv = np.full((x_pixels, y_pixels, 3),
                       default,
                       dtype=np.uint8)
    else:
        canv = backdrop.copy()
    for p in points:
        x = p[0]
        y = p[1]
        if x_range[0] <= x < x_range[1] - (1 / resolution) and y_range[0] <= y < y_range[1] - (1 / resolution):
            gradient = (p[2] - d) / A
            gradient = np.rint(255 * (gradient + 1) / 2).astype(int)
            x_addr = np.rint((x - x_range[0]) * resolution).astype(int)
            y_addr = np.rint((y - y_range[0]) * resolution).astype(int)
            canv[x_addr, y_addr] = (gradient, gradient, gradient)
    return canv


def video(frame_func, filename, t_range=(0, 10), FPS=5, frame_size='default'):
    if frame_size == 'default':
        frame_size = np.shape(frame_func(0))
    height = frame_size[0]
    width = frame_size[1]
    fourcc = cv2.VideoWriter_fourcc(*'MP42')
    video_writer = cv2.VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(FPS), (height, width))

    interval = t_range[1] - t_range[0]
    time = t_range[0]
    for _ in range(np.rint(FPS * interval).astype(int)):
        frame = frame_func(time)
        video_writer.write(frame)
        time += 1 / FPS

    video_writer.release()


# TODO rename. What to do about the one above?
def video2(frame_function, frame_arguments, filename, fps=5, preview=False, parallel=True):
    """
    Create a video with frames generated by applying the frame_func to each element in the frame_arguments list.
    Final video duration in seconds is len(frame_arguments)/fps

    :param frame_function: function called to generate a frame of the video using a frame_argument
    :param frame_arguments: list of arguments used to generate each frame of the video
    :param filename:
    :param fps:
    :param parallel:
    """
    image0 = frame_function(frame_arguments[0])
    if preview:
        hl.render_from_array(image0)
        mid = int(len(frame_arguments) / 2)
        hl.render_from_array(frame_function(frame_arguments[mid]))
        hl.render_from_array(frame_function(frame_arguments[-1]))

    frame_size = np.shape(image0)
    is_color = len(frame_size) > 2 and frame_size[2] > 1
    h = frame_size[0]
    w = frame_size[1]

    fourcc = cv2.VideoWriter_fourcc(*'MP42')
    video_writer = cv2.VideoWriter('{0}.avi'.format(filename), fourcc, float(fps), (h, w), isColor=is_color)

    # Create threads to render frames in parallel. Store rendered frames in a list
    # When each pool is spawned, they are in a new python environment. They must call a function that exists in
    # their thread, here global_function. Each pool is initialized to set the global_function to frame_func
    # TODO Use pathos to solve this problem. It can pickle functions so the global function pattern can be dropped
    if parallel:
        with Pool(initializer=set_global_function, initargs=(frame_function,)) as pool:
            frames = pool.map(call_global_function, frame_arguments[1:])
    # OpenCV sometimes crashed with multiprocess!
    else:
        frames = map(frame_function, frame_arguments[1:])

    # Create a video of the rendered frames
    for frame in [image0, *frames]:
        video_writer.write(frame.astype(np.uint8))

    video_writer.release()
    print("Wrote video {}".format(filename))


def interpolation_video(value_function,
                        t_param,
                        t_range,
                        frames,
                        fps,
                        frame_size,
                        file_prefix="./videos/",
                        geometric_interp=False,
                        preview=True,
                        parallel=True,
                        **kwargs):
    """
    Create a video using the frame function by interpolating :t_param: over :t_range: with :frames: steps.
    TODO: Allow multivariable interpolation?

    """
    function_name = value_function.__name__

    def frame_func(t):
        return sampling_image(value_function, image_size=frame_size, **{t_param: t}, **kwargs)

    if geometric_interp:
        frame_arguments = hl.np.geomspace(*t_range, num=frames)
    else:
        frame_arguments = hl.np.linspace(*t_range, num=frames)

    filename = file_prefix + "{}_{}={}-{}_frames={}_fps={}".format(function_name, t_param, *t_range, frames, fps)
    hl.video2(frame_function=frame_func, frame_arguments=frame_arguments, fps=fps, filename=filename,
              parallel=parallel, preview=preview)


# TODO Rename? Duplicate behavior?
# TODO CV functions crash multitreadding on macOS
def sampling_image(value_function,
                   value_range=(-1, 1),
                   image_size=(500, 500),
                   resolution=None,
                   binary=False,
                   **params):
    """
    Create an image by sampling point on a mesh across x_range and y_range.
    If the mesh resolution is smaller than the final image size, it is scaled.

    :param value_function: Function which takes a 2d array [x,y] and **params and returns a scalar or a len3 color array
    :param value_range: Float 2tuple or 2d array of x range, y range. Range to evaluate the function over
    :param image_size: Int 2tuple. Size of the final image array
    :param resolution: Scalar or 2tuple. The number of points to sample from range in the x and y directions
        defaults to image_size
    :param binary: Boolean. Whether or not
    :param params: additional params which should be passed to the value_function
    :return: uint8 image array in 1 or 3 channels, depending on the value_function
    """
    if resolution is None:
        resolution = image_size
    print("Creating image with resolution:{}, {}".format(resolution, params))

    resolution_x = resolution[0] if isinstance(resolution, collections.abc.Sequence) else resolution
    resolution_y = resolution[1] if isinstance(resolution, collections.abc.Sequence) else resolution
    value_range_x = value_range[0] if isinstance(value_range[0], collections.abc.Sequence) else value_range
    value_range_y = value_range[1] if isinstance(value_range[0], collections.abc.Sequence) else value_range

    x_axis = hl.np.linspace(start=value_range_x[0], stop=value_range_x[1], num=int(resolution_x))
    y_axis = hl.np.linspace(start=value_range_y[0], stop=value_range_y[1], num=int(resolution_y))

    # (x, y) for x in x_axis, y in y_axis
    meshgrid = hl.np.meshgrid(x_axis, y_axis)
    xy = hl.np.stack(meshgrid, axis=2)
    # Dimensions: (len(x_axis), len(y_axis), 2)

    # Apply the value function to each (x,y) in the grid. Might return a value or a [B,G,R]
    image_values = hl.np.apply_along_axis(lambda p: value_function(p, **params), 2, xy)

    # Normalised [0,255] as integer
    image = hl.np.interp(image_values, (image_values.min(), image_values.max()), (0, 255)).astype(hl.np.uint8)
    if binary:
        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Scale resolution to image size
    image = cv2.resize(image, image_size, interpolation=cv2.INTER_NEAREST)
    # These cv2 functions won't work with multiprocessing! WHY? It crashed my python

    return image
