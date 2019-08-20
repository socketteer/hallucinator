import numpy as np
import hallucinator


def obj_to_set(obj, params, region_type='path', density=5):
    if isinstance(obj, hallucinator.Group):
        points = set()
        for component in obj.components:
            new_points = obj_to_set(component, params, region_type, density)
            if new_points:
                points = points.union(new_points)
        return points
    else:
        return obj.region(region_type)(at=obj.at, params=params, density=density)


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


#TODO give params default value
#TODO function for reused code
def path_region(at, params, path_range, path_length="auto",
                p_name='p',
                density=1):
    """
    :param at: f(p) -> (x, y, ( , gradient, or (R, G, B)))
    :param params: anything
    :param path_range: (path_i, path_f)
    :param path_length: geometric length of path
    :param p_name: name of parameter
    :param density: num points to evaluate per range unit
    :return: set of points (x, y, ( , gradient, or (R, G, B)))
    """
    if path_length=='auto':
        path_length = path_range[1] - path_range[0]
    points = set()
    for eval_at in np.linspace(path_range[0], path_range[1], path_length*density):
        params[p_name] = eval_at
        points.add(at(params))

    return points


def surface_region(at, params, a_range, b_range,
                   a_length='auto',
                   b_length='auto',
                   a_name='a',
                   b_name='b',
                   density=1):
    """

    :param at:
    :param params:
    :param a_range:
    :param b_range:
    :param a_length:
    :param b_length:
    :param a_name:
    :param b_name:
    :param density:
    :return:
    """
    points = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]
    for a in np.linspace(a_range[0], a_range[1], a_length * density):
        for b in np.linspace(b_range[0], b_range[1], b_length * density):
            params[a_name] = a
            params[b_name] = b
            points.add(at(params))

    return points


def wireframe(at, params, a_range, b_range, a_spacing=3, b_spacing=3,
              a_length='auto', b_length='auto', density=1, a_name='a', b_name='b'):
    points = set()
    if a_length=='auto':
        a_length = a_range[1] - a_range[0]
    if b_length=='auto':
        b_length = b_range[1] - b_range[0]
    for a in np.linspace(a_range[0], a_range[1], a_length / a_spacing):
        for b in np.linspace(b_range[0], b_range[1], b_length * density):
            params[a_name] = a
            params[b_name] = b
            points.add(at(params))
    for b in np.linspace(b_range[0], b_range[1],b_length / b_spacing):
        for a in np.linspace(a_range[0], a_range[1], a_length * density):
            params[a_name] = a
            params[b_name] = b
            points.add(at(params))
    return points


def conditional_region(at, params, conditions, a_range, b_range,
                       a_name='a',
                       b_name='b',
                       density=1):
    """

    :param at:
    :param params:
    :param conditions:
    :param a_range:
    :param b_range:
    :param a_name:
    :param b_name:
    :param density:
    :return:
    """
    points = set()
    for a in np.linspace(a_range[0], a_range[1], (a_range[1] - a_range[0]) * density):
        for b in np.linspace(b_range[0], b_range[1], (b_range[1] - b_range[0]) * density):
            if all(condition(a, b) for condition in conditions):
                params[a_name] = a
                params[b_name] = b
                points.add(at(params))

    return points

