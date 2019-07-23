import numpy as np
import hallucinator


def obj_to_set(obj, params, density=5):
    if isinstance(obj, hallucinator.Group):
        points = set()
        for component in obj.components:
            new_points = obj_to_set(component, params, density)
            if new_points:
                points = points.union(new_points)
        return points
    else:
        return obj.region(at=obj.at, params=params, density=density)


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


"""gradient regions"""


def path_region(at, params, path_range, path_length="auto", density=1):
    """
    :param at: f(p) -> (x, y, ( , gradient, or (R, G, B)))
    :param params: anything
    :param path_range: (path_i, path_f)
    :param path_length: geometric length of path
    :param density: num points to evaluate per range unit
    :return: set of points (x, y, ( , gradient, or (R, G, B)))
    """
    if path_length=='auto':
        path_length = path_range[1] - path_range[0]
    points = set()
    for eval_at in np.linspace(path_range[0], path_range[1], path_length*density):
        params['p'] = eval_at
        points.add(at(params))

    return points


#TODO adapt these to new system
def rectangle_region(at, params, a_range, b_range,
                     a_length='auto',
                     b_length='auto',
                     density=1):
    points = set()
    if a_length=='auto':
        a_length = a_range[1] - a_range[0]
    if b_length=='auto':
        b_length = b_range[1] - b_range[0]
    for a in np.linspace(a_range[0], a_range[1], a_length * density):
        for b in np.linspace(b_range[0], b_range[1], b_length * density):
            params['a'] = a
            params['b'] = b
            points.add(at(params))

    return points


def conditional_region(at, params, conditions, a_range, b_range, density=1):
    points = set()
    for a in np.linspace(a_range[0], a_range[1], (a_range[1] - a_range[0]) * density):
        for b in np.linspace(b_range[0], b_range[1], (b_range[1] - b_range[0]) * density):
            if all(condition(a, b) for condition in conditions):
                params['a'] = a
                params['b'] = b
                points.add(at(params))

    return points

