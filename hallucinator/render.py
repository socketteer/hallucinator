from pathos.multiprocessing import ProcessingPool

import cv2
import matplotlib
import numpy as np
from PIL import Image
from bresenham import bresenham
from skimage import draw

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


# TODO Add opencv converters in imagify?
# class ImageStyle(Enum):
#     HSV = ...
#     BINARY = ...
def imagify(arr, bwref=None, **kwargs):
    normalized = hl.normalize_array(arr, from_range=bwref, to_range=(0, 255)).astype(np.uint8)
    if kwargs.get("hsv", False):
        # # Need a 3 channel image from [0,1]. Use the original array as H, S,V=1
        # arr = hl.normalize_array(arr, from_range=bwref)
        # ones = np.ones_like(arr).astype(np.uint8)
        # arr = np.stack([arr, ones, ones], -1)
        # #arr = matplotlib.colors.hsv_to_rgb(arr)
        # return hl.normalize_array(arr, from_range=(0, 1), to_range=(0, 255)).astype(np.uint8)

        # TODO opencv color converting. Doesn't work with process pools on mac python3.7. Works on 3.8?
        #   https://github.com/opencv/opencv/issues/5150
        ones = 255*np.ones_like(arr)
        arr = np.stack([normalized, ones, ones], -1)
        return cv2.cvtColor(arr, cv2.COLOR_HSV2BGR)
    else:
        return normalized

def contour_image(arr, **kwargs):
    hl.contour(arr, threshold=2*math.pi)
    return hl.imagify(arr, bwref=[0, 2*math.pi])

def save_img(data, filename):
    img = Image.fromarray(np.rot90(data))
    img.save(filename)


# TODO test existing canvas
def points_to_bichrome(points, x_range, y_range, foreground=WHITE, background=BLACK, resolution=5, backdrop="new"):
    """
    :param points: array of points (x, y) to draw in foreground color
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

            x1 = np.rint((l[0][0] - x_range[0]) * resolution).astype(int)
            y1 = np.rint((l[0][1] - y_range[0]) * resolution).astype(int)
            x2 = np.rint((l[1][0] - x_range[0]) * resolution).astype(int)
            y2 = np.rint((l[1][1] - y_range[0]) * resolution).astype(int)

            xs, ys = draw.line(x1, y1, x2, y2)
            for x, y in zip(xs, ys):
                try:
                    canv[x, y] = foreground  # x, y may be reversed
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


def _deprecated_video(frame_func, filename, t_range=(0, 10), FPS=5, frame_size='default'):
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


def video(frame_function, frame_arguments, filename, fps=5, preview=False, parallel_frames=True):
    """
    Create a video with frames generated by applying the frame_func to each element in the frame_arguments list.
    Final video duration in seconds is len(frame_arguments)/fps

    :param frame_function: function called to generate a frame of the video using a frame_argument
        frames should be 1 or 3 channel arrays from [0, 255]
    :param frame_arguments: list of arguments used to generate each frame of the video
    :param filename:
    :param fps:
    :param parallel:
    """
    if preview:
        hl.render_from_array(frame_function(frame_arguments[0]))
        mid = int(len(frame_arguments) / 2)
        hl.render_from_array(frame_function(frame_arguments[mid]))
        hl.render_from_array(frame_function(frame_arguments[-1]))

    # Create threads to render frames in parallel. Store rendered frames in a list
    if parallel_frames:
        with ProcessingPool() as pool:
            frames = pool.map(frame_function, frame_arguments[1:])
    # OpenCV sometimes crashed with multiprocess!
    else:
        frames = list(map(frame_function, frame_arguments[1:]))

    frame_size = np.shape(frames[0])
    is_color = len(frame_size) > 2 and frame_size[2] > 1
    h = frame_size[0]
    w = frame_size[1]
    fourcc = cv2.VideoWriter_fourcc(*'MP42')
    video_writer = cv2.VideoWriter('{0}.avi'.format(filename), fourcc, float(fps), (w, h), isColor=is_color)

    # Create a video of the rendered frames. Have to transpose rows and columns for the video writer...
    # https://github.com/opencv/opencv/issues/4655
    # TODO Don't do it like this. It will flip the image
    for frame in frames:
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
    hl.video(frame_function=frame_func, frame_arguments=frame_arguments, fps=fps, filename=filename,
             parallel_frames=parallel, preview=preview)



def sampling_image(value_function,
                   value_range=(-1, 1),
                   image_size=(500, 500),
                   bw_ref=None,
                   resolution=None,
                   binary=False,
                   parallel_sample=False,
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

    xy = hl.xy_plane(value_range, resolution)

    # Apply the value function to each (x,y) in the grid. Might return a value or a [B,G,R]
    if parallel_sample:
        # Flatten into array of 2d points [(x,y), ...]
        points = xy.reshape(-1, xy.shape[-1])
        with ProcessingPool() as pool:
            values = pool.map(lambda p: value_function(p, **params), points)
        image_values = np.resize(values, xy.shape[:-1])  # TODO Doesn't work with color arrays
    else:
        image_values = hl.np.apply_along_axis(lambda p: value_function(p, **params), 2, xy)

    # Normalised [0,255] as integer
    image = imagify(image_values, bw_ref)
    if binary:
        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Scale resolution to image size
    image = cv2.resize(image, image_size, interpolation=cv2.INTER_NEAREST)
    # These cv2 functions won't work with multiprocessing! WHY? It crashed my python

    return image