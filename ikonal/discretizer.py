import numpy as np
import ikonal


#TODO evaluate 2d parametric surface in 3 dimensions
def para_to_array(x_min, x_max, y_min, y_max, func, path,
                  num_points="default", resolution=50):
    if np.ndim(path) == 1:
        if num_points == "default":
            num_points = path[1] - path[0];
        arr = np.zeros((x_max - x_min, y_max - y_min), dtype=np.bool)
        for i in np.linspace(path[0], path[1], num_points):
            x, y = np.rint(func(i)).astype(int)
            if x_min <= x < x_max and y_min <= y < y_max:
                arr[x-x_min, y-y_min] = 1
        return arr
    elif np.ndim(path) == 2:
        #TODO resolution
        if num_points == "default":
            pts_horiz = path[0][1] - path[0][0]
            pts_vert = path[1][1] - path[1][0]
        else:
            pts_horiz = num_points[0]
            pts_vert = num_points[1]

        arr = np.zeros((x_max - x_min, y_max - y_min), dtype=np.bool)
        for i in np.linspace(path[0][0], path[0][1], pts_horiz):
            for j in np.linspace(path[1][0], path[1][1], pts_vert):
                x, y = np.rint(func(i, j)).astype(int)
                if x_min <= x < x_max and y_min <= y < y_max:
                    arr[x-x_min, y-y_min] = 1
        return arr


def obj_to_set(obj, density=5):
    if isinstance(obj, ikonal.Group):
        points = set()
        for component in obj.components:
            points = points.union(obj_to_set(component, density))
        return points
    elif isinstance(obj, ikonal.ParaObject):
        return para_to_set(obj.func, obj.path, obj.length, density)


def para_to_set(func, path, length, density=5):
    points = set()
    for i in np.linspace(path[0], path[1], density*length):
        points.add(func(i))
    print(len(points))
    return points


def phasegrid(func, x_range, y_range, resolution=5):
    x_size = x_range[1] - x_range[0]
    y_size = y_range[1] - y_range[0]

    arr = np.zeros((x_size*resolution, y_size*resolution), dtype=np.float)

    i = 0
    j = 0
    for x in np.linspace(x_range[0], x_range[1], x_size*resolution):
        for y in np.linspace(y_range[0], y_range[1], y_size*resolution):
            arr[i][j] = func(x, y)
            j += 1
        j = 0
        i += 1
    return arr


"""REGIONS"""


def path_region(f, path, p_range, density=1):
    """
    :param f: (x, y) -> phase
    :param path: p -> (x, y)
    :param p_range: (pi, pf)
    :param density: num points to evaluate per range unit
    :return: set of points (x, y, phase)
    """
    path_length = p_range[1] - p_range[0]
    points = set()
    for p in np.linspace(p_range[0], p_range[1], path_length*density):
        x, y = path(p)
        points.add(f(x, y))

    return points


def rectangle_region(f, x_range, y_range, density=1):
    points = set()
    for x in np.linspace(x_range[0], x_range[1], (x_range[1] - x_range[0]) * density):
        for y in np.linspace(y_range[0], y_range[1], (y_range[1] - y_range[0]) * density):
            points.add(f(x, y))

    return points


def conditional_region(f, conditions, x_range, y_range, density=1):
    points = set()
    for x in np.linspace(x_range[0], x_range[1], (x_range[1] - x_range[0]) * density):
        for y in np.linspace(y_range[0], y_range[1], (y_range[1] - y_range[0]) * density):
            if all(condition(x, y) for condition in conditions):
                points.add(f(x, y))

    return points




#TODO para surface

