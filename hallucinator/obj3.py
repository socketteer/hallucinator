import math
import hallucinator
import operator
import numpy as np

'''parametric functions'''


def line_3(p0, dx, dy, dz):
    return lambda p: (p0[0] + p * dx, p0[1] + p * dy, p0[2] + p * dz)


def plane(p0, v1, v2):
    p0 = np.asarray(p0)
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)
    return lambda a, b: tuple(p0 + a * v1 + b * v2)


'''object primitives'''


def vector_3(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    z_len = z2 - z1
    distance = math.sqrt(x_len ** 2 + y_len ** 2 + z_len ** 2)
    region = lambda at, params, density: hallucinator.path_region(at=at,
                                                                  params=params,
                                                                  path_range=(0, distance),
                                                                  path_length=distance,
                                                                  density=density)
    return hallucinator.ParaObject3(line_3(p1, x_len / distance, y_len / distance, z_len / distance),
                                    region=region,
                                    species='3vector')


def path_3(path_func, p_range, path_length="auto"):
    def region(at, params, density): return hallucinator.path_region(at=at,
                                                                     params=params,
                                                                     path_range=p_range,
                                                                     path_length=path_length,
                                                                     density=density)

    return hallucinator.ParaObject3(path_func, region=region, species="path")


def ellipse_3(h, w):
    pass


def plane_section(p0=(0, 0, 0), v1=(0, 1, 0), v2=(1, 0, 0), a_range=(0, 1), b_range=(0, 1)):
    a_length = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    b_length = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)
    region = lambda at, params, density: hallucinator.rectangle_region(at=at,
                                                                       params=params,
                                                                       a_range=a_range,
                                                                       b_range=b_range,
                                                                       a_length=a_length,
                                                                       b_length=b_length,
                                                                       density=density)
    return hallucinator.ParaObject3(plane(p0, v1, v2),
                                    region=region,
                                    species='plane')


#TODO combine with near-identical 2 function
def disturbance_on_path_3(disturbance, v, init_pos, polarization, path, p_range, path_length="auto"):
    """
    :param disturbance:
    :param v:
    :param init_pos:
    :param polarization:
    :param path:
    :param p_range:
    :param path_length:
    :return:
    """

    def f(p, t): return tuple(np.add((disturbance(p - init_pos - v * t) * np.asarray(polarization)), path(p)))

    def region(at, params, density): return hallucinator.path_region(at=at,
                                                                     params=params,
                                                                     path_range=p_range,
                                                                     path_length=path_length,
                                                                     density=density)

    return hallucinator.ParaObject3(f,
                                    region=region,
                                    species='disturbance_on_path')


def textured_path(texture, pos, polarization, path, p_range, path_length):
    def f(p): return tuple(np.add((texture(p - pos) * np.asarray(polarization)), path(p)))

    def region(at, params, density): return hallucinator.path_region(at=at,
                                                                     params=params,
                                                                     path_range=p_range,
                                                                     path_length=path_length,
                                                                     density=density)

    return hallucinator.ParaObject3(f,
                                    region=region,
                                    species='textured_path')


def surface(surface_func, a_range, b_range, a_length='auto', b_length='auto'):

    def region(at, params, density): return hallucinator.rectangle_region(at=at,
                                                                          params=params,
                                                                          a_range=a_range,
                                                                          b_range=b_range,
                                                                          a_length=a_length,
                                                                          b_length=b_length,
                                                                          density=density)

    return hallucinator.ParaObject3(surface_func,
                                    region=region,
                                    species='surface')


def disturbance_on_surface(disturbance, v, init_pos, polarization, surface, a_range, b_range,
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
    def f(a, b, t): return tuple(np.add((disturbance(math.sqrt((init_pos[0] - a) ** 2 + (init_pos[1] - b) ** 2) - v * t)
                                         * np.asarray(polarization)),
                                        surface(a, b)))

    def region(at, params, density): return hallucinator.rectangle_region(at=at,
                                                                          params=params,
                                                                          a_range=a_range,
                                                                          b_range=b_range,
                                                                          a_length=a_length,
                                                                          b_length=b_length,
                                                                          density=density)

    return hallucinator.ParaObject3(f,
                                    region=region,
                                    species='disturbance_on_surface')


'''groups'''


def rectangle_3(h, w):
    pass


def box(h, w, d, p0=(0, 0, 0)):
    b = hallucinator.Group3(species='box')
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
    ax = hallucinator.Group3(species='3axes')
    ax.add_component(vector_3((origin[0] + x_range[0], origin[1], origin[2]),
                              (origin[0] + x_range[1], origin[1], origin[2])))
    ax.add_component(vector_3((origin[0], origin[1] + y_range[0], origin[2]),
                              (origin[0], origin[1] + y_range[1], origin[2])))
    ax.add_component(vector_3((origin[0], origin[1], origin[2] + z_range[0]),
                              (origin[0], origin[1], origin[2] + z_range[1])))

    return ax
