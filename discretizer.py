import numpy as np


def para_to_array(x_min, x_max, y_min, y_max, func, path_start, path_end, num_points="default"):
    if num_points == "default":
        num_points = path_end - path_start
    arr = np.zeros((x_max - x_min, y_max - y_min), dtype=np.bool)
    for i in np.linspace(path_start, path_end, num_points):
        x, y = np.rint(func(i)).astype(int)
        if x_min <= x < x_max and y_min <= y < y_max:
            arr[x-x_min, y-y_min] = 1
    return arr


def para_to_set(func, path_start, path_end, num_points="default"):
    if num_points == "default":
        num_points = path_end - path_start
    points = set()
    for i in np.linspace(path_start, path_end, num_points):
        x, y = np.rint(func(i)).astype(int)
        points.add((x, y))
    return points




