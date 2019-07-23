import hallucinator
import copy
import math
import numpy as np

'''parametric functions'''


def line(p0, dx, dy):
    return lambda p: (p0[0] + p * dx, p0[1] + p * dy)


def circle_parametric(r, c):
    return lambda p: (r * math.cos(p) + c[0], r * math.sin(p) + c[1])


'''object primitives'''


# TODO do not write length in stone, but deal with this later
def vector(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    distance = math.hypot(x_len, y_len)

    def region(at, params, density): return hallucinator.path_region(at=at,
                                                                     params=params,
                                                                     path_range=(0, distance),
                                                                     path_length=distance,
                                                                     density=density)

    return hallucinator.ParaObject2(line(p1, x_len / distance, y_len / distance),
                                    region=region,
                                    species='vector')


def circle_primitive(r, c):
    def region(at, params, density): return hallucinator.path_region(at=at,
                                                                     params=params,
                                                                     path_range=(0, 2 * math.pi),
                                                                     path_length=2 * math.pi * r,
                                                                     density=density)

    return hallucinator.ParaObject2(circle_parametric(r, c),
                                    region=region,
                                    species='circle')


def ellipse():
    pass


def path(path_func, p_range, path_length="auto"):
    def region(at, params, density): return hallucinator.path_region(at=at,
                                                                     params=params,
                                                                     path_range=p_range,
                                                                     path_length=path_length,
                                                                     density=density)
    return hallucinator.ParaObject2(path_func, region=region, species="path")


#TODO polarization varies with p
#TODO start time
def disturbance_on_path(disturbance, v, init_pos, polarization, path, p_range, path_length="auto"):
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

    return hallucinator.ParaObject2(f,
                                    region=region,
                                    species='disturbance_on_path')


def textured_path(texture, pos, polarization, path, p_range, path_length):
    def f(p): return tuple(np.add((texture(p - pos) * np.asarray(polarization)), path(p)))

    def region(at, params, density): return hallucinator.path_region(at=at,
                                                                     params=params,
                                                                     path_range=p_range,
                                                                     path_length=path_length,
                                                                     density=density)

    return hallucinator.ParaObject2(f,
                                    region=region,
                                    species='textured_path')


'''groups'''


# TODO with transforms instead
# TODO remove p0?
def rectangle(h, w, p0):
    rect = hallucinator.Group(species='rectangle')
    rect.add_component(vector((p0[0], p0[1]), (p0[0], p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1]), (p0[0] + w, p0[1])))
    rect.add_component(vector((p0[0] + w, p0[1]), (p0[0] + w, p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1] + h), (p0[0] + w, p0[1] + h)))
    return rect


def square(w, p0):
    return rectangle(w, w, p0)


def polygon(w, n):
    poly = hallucinator.Group(species='{0}_gon'.format(n))
    side = vector((0, 0), (w, 0))
    pivot = 1
    angle = (n - 2) * math.pi / n
    for i in range(n):
        poly.add_component(copy.deepcopy(side))
        end = side.eval_at(w if pivot else 0)[0:2]
        side = side.rotate(theta=-angle, p=end)
        pivot = not pivot
    return poly


def axes(x_range, y_range, origin=(0, 0)):
    ax = hallucinator.Group(species='axes')
    ax.add_component(vector((origin[0] + x_range[0], origin[1]), (origin[0] + x_range[1], origin[1])))
    ax.add_component(vector((origin[0], origin[1] + y_range[0]), (origin[0], origin[1] + y_range[1])))
    return ax
