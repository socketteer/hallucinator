from multiprocessing.pool import Pool

import numpy as np
from PIL import Image
from cv2 import VideoWriter, VideoWriter_fourcc
from bresenham import bresenham

from hallucinator.utility import set_global_function, call_global_function

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (127, 127, 127)


def canvas(w, h, color=BLACK):
    canv = np.full( (w, h, 3), color, dtype=np.uint8)
    return canv


def render_from_array(data):
    img = Image.fromarray(np.rot90(data))
    img.show()


def save_img(data, filename):
    img = Image.fromarray(np.rot90(data))
    img.save('./images/{0}.jpg'.format(filename))


#TODO test existing canvas
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
        canv = np.full(((x_range[1] - x_range[0])*resolution,
                        (y_range[1] - y_range[0])*resolution,
                        3),
                       background, dtype=np.uint8)
    else:
        canv = backdrop.copy()
    for p in points:
        x = p[0]
        y = p[1]
        if x_range[0] <= x < x_range[1]-(1 / resolution) and y_range[0] <= y < y_range[1]-(1 / resolution):
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
                    #print('index error')
                    pass
    return canv


#test for weird things like black and white switched
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


#TODO make methods from reused functionality
#TODO need range-1 here too for rounding?
def set_to_gradient(points, x_range, y_range, black_ref=-1.0, white_ref=1.0, default=BLUE, resolution=5, backdrop="new"):
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
    if backdrop == "new":
        canv = np.full(((x_range[1] - x_range[0])*resolution,
                        (y_range[1] - y_range[0])*resolution, 3),
                       default,
                       dtype=np.uint8)
    else:
        canv = backdrop.copy()
    for p in points:
        x = p[0]
        y = p[1]
        if x_range[0] <= x < x_range[1]-(1 / resolution) and y_range[0] <= y < y_range[1]-(1/resolution):
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
    fourcc = VideoWriter_fourcc(*'MP42')
    video_writer = VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(FPS), (height, width))

    interval = t_range[1] - t_range[0]
    time = t_range[0]
    for _ in range(np.rint(FPS * interval).astype(int)):
        frame = frame_func(time)
        video_writer.write(frame)
        time += 1 / FPS

    video_writer.release()


def parallel_video(frame_func, filename, t_range=(0, 10), frames=50, fps=5, frame_size='default', is_color=False):
    if frame_size == 'default':
        frame_size = np.shape(frame_func(0))
    h = frame_size[0]
    w = frame_size[1]
    fourcc = VideoWriter_fourcc(*'MP42')
    video_writer = VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(fps), (h, w), isColor=is_color)

    t_steps = np.linspace(*t_range, frames)
    # Create threads to render frames in parallel. Store rendered frames in a list
    # When each pool is spawned, they are in a new python environment. They must call a function that exists in
    # their thread, here global_function. Each pool is initialized to set the global_function to frame_func
    with Pool(None, initializer=set_global_function, initargs=(frame_func,)) as pool:
        frames = pool.map(call_global_function, t_steps)

    # Create a video of the rendered frames
    for frame in frames:
        video_writer.write(frame)

    video_writer.release()
    print("Wrote video {}".format(filename))


def create_image(value_function, params, x_range=(-1, 1), y_range=(-1, 1), image_width=500):
    print("Creating image with {}".format(params))
    x_axis = np.linspace(start=x_range[0], stop=x_range[1], num=image_width)
    y_axis = np.linspace(start=y_range[0], stop=y_range[1], num=image_width)

    # (x, y) for x in x_axis, y in y_axis
    meshgrid = np.meshgrid(x_axis, y_axis)
    xy = np.stack(meshgrid, axis=2)
    # Dimensions: (len(x_axis), len(y_axis), 2)

    # Apply the value function to each (x,y) in the grid. Might return a value or a [B,G,R]
    image_values = np.apply_along_axis(lambda p: value_function(p, **params), 2, xy)

    # Normalised [0,255] as integer
    image = np.interp(image_values, (image_values.min(), image_values.max()),
                      (0, 255)).astype(np.uint8)

    # If a single value was given, expand the array to dimensions: (len(x_axis), len(y_axis), 3)
    # if len(image.shape) == 2:
    #     image = hl.np.repeat(image[:, :, hl.np.newaxis], 3, axis=2)

    # hl.render_from_array(image)
    return image


def line(x0, x1, y0, y1):
    return list(bresenham(x0, x1, y0, y1))
