import numpy as np
from PIL import Image
from cv2 import VideoWriter, VideoWriter_fourcc
from bresenham import bresenham


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
    video = VideoWriter('./videos/{0}.avi'.format(filename), fourcc, float(FPS), (height, width))

    interval = t_range[1] - t_range[0]
    time = t_range[0]
    for _ in range(np.rint(FPS * interval).astype(int)):
        frame = frame_func(time)
        video.write(frame)
        time += 1 / FPS

    video.release()


def line(x0, x1, y0, y1):
    return list(bresenham(x0, x1, y0, y1))
