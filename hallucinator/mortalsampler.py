import numpy as np


def path_points(path_range, path_length='auto', density=1):
    if path_length == 'auto':
        path_length = path_range[1] - path_range[0]
    num_points = int(round(path_length*density))
    points = np.linspace(path_range[0], path_range[1], num=num_points)
    return points


def surface_points(surface_range, length=('auto', 'auto'), density=(1, 1)):
    length = list(length)
    if length[0] == 'auto':
        length[0] = surface_range[0][1] - surface_range[0][0]
    if length[1] == 'auto':
        length[1] = surface_range[1][1] - surface_range[1][0]
    num_points_a = int(round(length[0] * density[0]))
    num_points_b = int(round(length[1] * density[1]))
    a_axis = np.linspace(surface_range[0][0], surface_range[0][1], num=num_points_a)
    b_axis = np.linspace(surface_range[1][0], surface_range[1][1], num=num_points_b)
    meshgrid = np.meshgrid(a_axis, b_axis)
    ab = np.stack(meshgrid, axis=2)
    return ab


def eval_path(f, points):
    f = np.vectorize(f)
    return np.array(f(points))


def eval_surf(f, a_axis, b_axis):
    f = np.vectorize(f)
    pts = np.array(f(a_axis[:, None], b_axis[None, :]))
    pts = pts.reshape((pts.shape[0], pts.shape[1]*pts.shape[2]))
    return pts


# TODO give params default value
# TODO function for reused code
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
    if path_length == 'auto':
        path_length = path_range[1] - path_range[0]
    points = set()
    for eval_at in np.linspace(path_range[0], path_range[1], num=int(round(path_length * density))):
        params[p_name] = eval_at
        points.add(at(params))

    return points


def surface_region(at, params, a_range, b_range,
                   a_length='auto',
                   b_length='auto',
                   a_name='a',
                   b_name='b',
                   a_density=1,
                   b_density=1):
    points = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]
    for a in np.linspace(a_range[0], a_range[1], a_length * a_density):
        for b in np.linspace(b_range[0], b_range[1], b_length * b_density):
            params[a_name] = a
            params[b_name] = b
            points.add(at(params))

    # print(points)
    return points


def surface_region_random(at, params, a_range, b_range,
                          a_name='a',
                          b_name='b',
                          density=1):
    pass


def wireframe(at, params, a_range, b_range, a_spacing=3, b_spacing=3,
              a_length='auto', b_length='auto', density=1, a_name='a', b_name='b'):
    points = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]
    for a in np.linspace(a_range[0], a_range[1], int(round(a_length / a_spacing))):
        for b in np.linspace(b_range[0], b_range[1], int(round(b_length * density))):
            params[a_name] = a
            params[b_name] = b
            points.add(at(params))
    for b in np.linspace(b_range[0], b_range[1], int(round(b_length / b_spacing))):
        for a in np.linspace(a_range[0], a_range[1], int(round(a_length * density))):
            params[a_name] = a
            params[b_name] = b
            points.add(at(params))
    return points


def wireframe_lines(at, params, a_range, b_range, a_spacing=0.5, b_spacing=0.5,
                    a_length='auto', b_length='auto', a_name='a', b_name='b',
                    toggle_a=True, toggle_b=True):
    lines = set()
    if a_length == 'auto':
        a_length = a_range[1] - a_range[0]
    if b_length == 'auto':
        b_length = b_range[1] - b_range[0]
    if toggle_a:
        for a in np.linspace(a_range[0], a_range[1] - a_spacing, int(round(a_length / a_spacing))):
            for b in np.linspace(b_range[0], b_range[1], int(round(b_length / b_spacing))):
                params[a_name] = a
                params[b_name] = b
                p1 = at(params)
                params[a_name] = a + a_spacing
                p2 = at(params)
                lines.add((p1, p2))
    # TODO need 2 loops?
    if toggle_b:
        for b in np.linspace(b_range[0], b_range[1] - b_spacing, int(round(b_length / b_spacing))):
            for a in np.linspace(a_range[0], a_range[1], int(round(a_length / a_spacing))):
                params[a_name] = a
                params[b_name] = b
                p1 = at(params)
                params[b_name] = b + b_spacing
                p2 = at(params)
                lines.add((p1, p2))

    return lines


def conditional_region(at, params, conditions, a_range, b_range,
                       a_name='a',
                       b_name='b',
                       density=1):
    points = set()
    for a in np.linspace(a_range[0], a_range[1], (a_range[1] - a_range[0]) * density):
        for b in np.linspace(b_range[0], b_range[1], (b_range[1] - b_range[0]) * density):
            if all(condition(a, b) for condition in conditions):
                params[a_name] = a
                params[b_name] = b
                points.add(at(params))

    return points
