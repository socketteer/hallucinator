import math
import hallucinator as hl
import numpy as np

'''parametric functions'''


def line_3(p0, dx, dy, dz):
    return lambda p: (p0[0] + p * dx, p0[1] + p * dy, p0[2] + p * dz)


def plane(p0, v1, v2):
    p0 = np.asarray(p0)
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)
    return lambda a, b: tuple(p0 + a * v1 + b * v2)


def spherical(center, radius):
    return lambda azimuth, polar: (radius * math.sin(polar) * math.cos(azimuth) + center[0],
                                   radius * math.sin(polar) * math.sin(azimuth) + center[1],
                                   radius * math.cos(polar) + center[2])


'''object primitives'''


def sphere(center, radius):
    return hl.ParaObject3(spherical(center, radius),
                          region_type='2d',
                          region_params={'a_range': (0, 2 * math.pi),
                                         'b_range': (0, math.pi),
                                         'a_length': (2 * math.pi * radius),
                                         'b_length': (math.pi * radius),
                                         'a_name': 'azimuth',
                                         'b_name': 'polar'},

                          species='sphere')


def vector_3(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    z_len = z2 - z1
    distance = math.sqrt(x_len ** 2 + y_len ** 2 + z_len ** 2)
    return hl.ParaObject3(line_3(p1, x_len / distance, y_len / distance, z_len / distance),
                          region_type='path',
                          region_params={'path_range': (0, distance),
                                         'path_length': distance},
                          species='3vector')


def path_3(path_func, p_range, path_length="auto"):
    return hl.ParaObject3(path_func, region_type='path',
                          region_params={'path_range': p_range,
                                         'path_length': path_length},
                          species="path")


def ellipse_3(h, w):
    pass


def plane_section(p0=(0, 0, 0), v1=(0, 1, 0), v2=(1, 0, 0), a_range=(0, 1), b_range=(0, 1)):
    a_length = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    b_length = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)
    return hl.ParaObject3(plane(p0, v1, v2),
                          region_type='2d',
                          region_params={'a_range': a_range,
                                         'b_range': b_range,
                                         'a_length': a_length,
                                         'b_length': b_length},
                          species='plane')


# TODO combine with near-identical 2 function
def disturbance_on_path_3(disturbance, init_pos, polarization, path, p_range, path_length="auto"):

    def f(p, t): return tuple(np.add((disturbance(p - init_pos, t) * np.asarray(polarization)), path(p)))

    return hl.ParaObject3(f,
                          region_params={'path_range': p_range,
                                         'path_length': path_length},
                          species='disturbance_on_path')


def textured_path(texture, pos, polarization, path, p_range, path_length):
    def f(p): return tuple(np.add((texture(p - pos) * np.asarray(polarization)), path(p)))

    return hl.ParaObject3(f,
                          region_params={'path_range': p_range,
                                         'path_length': path_length},
                          species='textured_path')


def surface(surface_func, a_range, b_range, a_length='auto', b_length='auto'):
    return hl.ParaObject3(surface_func,
                          region_type='2d',
                          region_params={'a_range': a_range,
                                         'b_range': b_range,
                                         'a_length': a_length,
                                         'b_length': b_length},
                          species='surface')


'''def disturbance_on_surface(disturbance, init_pos, polarization, surface, a_range, b_range,
                           a_length="auto",
                           b_length="auto"):
    """
    :param disturbance:
    :param v:
    :param init_pos:
    :param polarization:
    :param surface:
    :param a_range:
    :param b_range:
    :param a_length:
    :param b_length:
    :return:
    """

    def f(a, b, t): return tuple(np.add((disturbance(a - init_pos[0], b - init_pos[1], t)
                                         * np.asarray(polarization)),
                                        surface(a, b)))

    return hl.ParaObject3(f,
                          region_type='2d',
                          region_params={'a_range': a_range,
                                         'b_range': b_range,
                                         'a_length': a_length,
                                         'b_length': b_length},
                          species='disturbance_on_surface')'''


# this is radial
def textured_surface(texture, pos, polarization, surface, a_range, b_range,
                     a_length="auto",
                     b_length="auto"):
    """
    :param texture:
    :param pos:
    :param polarization:
    :param surface:
    :param a_range:
    :param b_range:
    :param a_length:
    :param b_length:
    :return:
    """

    def f(a, b): return tuple(np.add((texture(math.sqrt((pos[0] - a) ** 2 + (pos[1] - b) ** 2))
                                      * np.asarray(polarization)),
                                     surface(a, b)))

    return hl.ParaObject3(f,
                          region_type='2d',
                          region_params={'a_range': a_range,
                                         'b_range': b_range,
                                         'a_length': a_length,
                                         'b_length': b_length},
                          species='textured_surface')


'''groups'''


def rectangle_3(h, w):
    rect = hl.Group3(species='rectangle')
    return rect


def box(h, w, d, p0=(0, 0, 0)):
    b = hl.Group3(species='box')
    b.add_component(vector_3(p0, (p0[0] + h, p0[1], p0[2])))
    b.add_component(vector_3(p0, (p0[0], p0[1] + w, p0[2])))
    b.add_component(vector_3(p0, (p0[0], p0[1], p0[2] + d)))
    b.add_component(vector_3((p0[0] + h, p0[1], p0[2]), (p0[0] + h, p0[1] + w, p0[2])))
    b.add_component(vector_3((p0[0] + h, p0[1], p0[2]), (p0[0] + h, p0[1], p0[2] + d)))
    b.add_component(vector_3((p0[0], p0[1] + w, p0[2]), (p0[0] + h, p0[1] + w, p0[2])))
    b.add_component(vector_3((p0[0], p0[1] + w, p0[2]), (p0[0], p0[1] + w, p0[2] + d)))
    b.add_component(vector_3((p0[0], p0[1], p0[2] + d), (p0[0] + h, p0[1], p0[2] + d)))
    b.add_component(vector_3((p0[0], p0[1], p0[2] + d), (p0[0], p0[1] + w, p0[2] + d)))
    b.add_component(vector_3((p0[0] + h, p0[1] + w, p0[2] + d), (p0[0] + h, p0[1] + w, p0[2])))
    b.add_component(vector_3((p0[0] + h, p0[1] + w, p0[2] + d), (p0[0] + h, p0[1], p0[2] + d)))
    b.add_component(vector_3((p0[0] + h, p0[1] + w, p0[2] + d), (p0[0], p0[1] + w, p0[2] + d)))
    return b


def axes_3(x_range, y_range, z_range, origin=(0, 0, 0)):
    ax = hl.Group3(species='3axes')
    ax.add_component(vector_3((origin[0] + x_range[0], origin[1], origin[2]),
                              (origin[0] + x_range[1], origin[1], origin[2])))
    ax.add_component(vector_3((origin[0], origin[1] + y_range[0], origin[2]),
                              (origin[0], origin[1] + y_range[1], origin[2])))
    ax.add_component(vector_3((origin[0], origin[1], origin[2] + z_range[0]),
                              (origin[0], origin[1], origin[2] + z_range[1])))

    return ax


def arrow_3(p0, direction, length=1, head_length='default'):
    pass


def point_lattice(points, connections, origin=(0, 0, 0)):
    """
    :param points: array of coordinates of points
    :param connections: list of pairs of connected points
    :param origin: all points are translated by origin
    :return:
    """
    lattice = hl.Group3(species='lattice')
    for pair in connections:
        point = points[pair[0]]
        point2 = points[pair[1]]
        lattice.add_component(vector_3((origin[0] + point[0], origin[1] + point[1], origin[2] + point[2]),
                                       (origin[0] + point2[0], origin[1] + point2[1], origin[2] + point2[2])))
    return lattice


def cross(width, depth, span, l_height, u_height, origin=(0, 0, 0)):
    points = ((0, 0, 0),
              (width, 0, 0),
              (0, depth, 0),
              (width, depth, 0),
              (0, 0, l_height),
              (width, 0, l_height),
              (0, depth, l_height),
              (width, depth, l_height),
              (-span, 0, l_height),
              (span + width, 0, l_height),
              (-span, depth, l_height),
              (span + width, depth, l_height),
              (0, 0, l_height + width),
              (width, 0, l_height + width),
              (0, depth, l_height + width),
              (width, depth, l_height + width),
              (-span, 0, l_height + width),
              (span+width, 0, l_height + width),
              (-span, depth, l_height + width),
              (span+width, depth, l_height + width),
              (0, 0, l_height + width + u_height),
              (width, 0, l_height + width + u_height),
              (0, depth, l_height + width + u_height),
              (width, depth, l_height + width + u_height))

    connections = ((0, 1), (0, 2), (1, 3), (2, 3),
                   (0, 4), (1, 5), (2, 6), (3, 7),
                   (8, 4), (5, 9), (8, 10), (9, 11),
                   (10, 6), (7, 11), (8, 16), (9, 17),
                   (10, 18), (11, 19), (16, 12), (17, 13),
                   (18, 16), (19, 17), (18, 14), (19, 15),
                   (12, 20), (13, 21), (14, 22), (15, 23),
                   (20, 21), (20, 22), (21, 23), (22, 23))

    return point_lattice(points=points, connections=connections, origin=origin)
