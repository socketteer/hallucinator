import hallucinator as hl
import copy
import math
import numpy as np

'''parametric functions'''


def line_parametric(p0, dx, dy):
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
    return hl.ParaObject2(line_parametric(p1, x_len / distance, y_len / distance),
                          region_params={'path_range': (0, distance),
                                         'path_length': distance},
                          species='vector')


def circle_primitive(r, c):
    return hl.ParaObject2(circle_parametric(r, c),
                          region_params={'path_range': (0, 2 * math.pi),
                                         'path_length': 2 * math.pi * r},
                          species='circle')


def ellipse():
    pass


def path(path_func, p_range, path_length="auto"):
    return hl.ParaObject2(path_func,
                          region_params={'path_range': p_range,
                                         'path_length': path_length},
                          species="path")

'''
# TODO polarization varies with p
# TODO start time
def disturbance_on_path(disturbance, init_pos, polarization, path, p_range, path_length="auto"):
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

    def f(p, t): return tuple(np.add((disturbance(p - init_pos, t) * np.asarray(polarization)), path(p)))

    return hl.ParaObject2(f,
                          region_params={'path_range': p_range,
                                         'path_length': path_length},
                          species='disturbance_on_path')'''


def textured_path(texture, pos, polarization, path, p_range, path_length):
    def f(p): return tuple(np.add((texture(p - pos) * np.asarray(polarization)), path(p)))

    return hl.ParaObject2(f,
                          region_params={'path_range': p_range,
                                         'path_length': path_length},
                          species='textured_path')


'''groups'''


# TODO with transforms instead
# TODO remove p0?
def rectangle(h, w, p0):
    rect = hl.Group(species='rectangle')
    rect.add_component(vector((p0[0], p0[1]), (p0[0], p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1]), (p0[0] + w, p0[1])))
    rect.add_component(vector((p0[0] + w, p0[1]), (p0[0] + w, p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1] + h), (p0[0] + w, p0[1] + h)))
    return rect


def square(w, p0):
    return rectangle(w, w, p0)


def polygon(w, n):
    poly = hl.Group(species='{0}_gon'.format(n))
    side = vector((0, 0), (w, 0))
    pivot = 1
    angle = (n - 2) * math.pi / n
    for i in range(n):
        poly.add_component(copy.deepcopy(side))
        end = side.eval_at(w if pivot else 0)[0:2]
        side = side.rotate(theta=-angle, p=end)
        pivot = not pivot
    return poly


def wheel(radius, num_spokes):
    w = hl.Group(species='wheel')
    for i in range(num_spokes):
        spoke = vector((0, 0), (radius, 0))
        spoke = spoke.rotate(theta=i*2*math.pi/num_spokes)
        w.add_component(spoke)
    w.add_component(circle_primitive(r=radius, c=(0, 0)))
    return w


def axes(x_range, y_range, origin=(0, 0)):
    ax = hl.Group(species='axes')
    ax.add_component(vector((origin[0] + x_range[0], origin[1]), (origin[0] + x_range[1], origin[1])))
    ax.add_component(vector((origin[0], origin[1] + y_range[0]), (origin[0], origin[1] + y_range[1])))
    return ax


def arrow(p0, direction, length=1, head_length=0):
    arw = hl.Group(species='arrow')
    direction = np.array(direction, copy=False)
    direction /= np.linalg.norm(direction)
    arw.add_component(hl.ParaObject2(line_parametric(p0, direction[0], direction[1]),
                                     region_params={'path_range': (-length / 2, length / 2),
                                                    'path_length': length},
                                     species='arrow_body'))
    if not head_length == 0:
        arrow_tip_coordinates = np.add(p0, np.asarray(direction) * (length / 2))
        arrowhead_dir_1 = np.matmul(hl.rotate(3 * math.pi / 4), direction + (1, ))
        arrowhead_dir_2 = np.matmul(hl.rotate(-3 * math.pi / 4), direction + (1, ))
        arw.add_component(hl.ParaObject2(line_parametric(arrow_tip_coordinates, arrowhead_dir_1[0], arrowhead_dir_1[1]),
                                         region_params={'path_range': (0, head_length),
                                                        'path_length': head_length},
                                         species='arrow_head'))

        arw.add_component(hl.ParaObject2(line_parametric(arrow_tip_coordinates, arrowhead_dir_2[0], arrowhead_dir_2[1]),
                                         region_params={'path_range': (0, head_length),
                                                        'path_length': head_length},
                                         species='arrow_head'))
    return arw
