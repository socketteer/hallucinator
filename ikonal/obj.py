import math
import ikonal
import copy
import math

'''parametric functions'''


def line(p0, dx, dy):
    return lambda p: (p0[0] + p * dx, p0[1] + p * dy, 1)


def circle_parametric(r, c):
    return lambda p: (r * math.cos(p) + c[0], r * math.sin(p) + c[1], 1)


'''object primitives'''


# TODO do not write length in stone, but deal with this later
def vector(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    distance = math.hypot(x_len, y_len)

    def region(at, params, density): return ikonal.path_region(at=at,
                                                               params=params,
                                                               path_range=(0, distance),
                                                               path_length=distance,
                                                               density=density)

    return ikonal.ParaObject2(line(p1, x_len / distance, y_len / distance),
                              region=region,
                              species='vector')


def circle_primitive(r, c):
    def region(at, params, density): return ikonal.path_region(at=at,
                                                               params=params,
                                                               path_range=(0, 2 * math.pi),
                                                               path_length=2 * math.pi * r,
                                                               density=density)

    return ikonal.ParaObject2(circle_parametric(r, c),
                              region=region,
                              species='circle')


def ellipse():
    pass


def wave_primitive(f, v, x_range=(0, 1)):
    def region(at, params, density): return ikonal.path_region(at=at,
                                                               params=params,
                                                               path_range=(x_range[0], x_range[1]),
                                                               path_length=x_range[1] - x_range[0],
                                                               density=density)

    return ikonal.ParaObject2(ikonal.propagating_disturbance(f, v),
                              region=region,
                              species='wave')


'''groups'''


# TODO with transforms instead
# TODO remove p0?
def rectangle(h, w, p0):
    rect = ikonal.Group(species='rectangle')
    rect.add_component(vector((p0[0], p0[1]), (p0[0], p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1]), (p0[0] + w, p0[1])))
    rect.add_component(vector((p0[0] + w, p0[1]), (p0[0] + w, p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1] + h), (p0[0] + w, p0[1] + h)))
    return rect


def square(w, p0):
    return rectangle(w, w, p0)


def polygon(w, n):
    poly = ikonal.Group(species='{0}_gon'.format(n))
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
    ax = ikonal.Group(species='axes')
    ax.add_component(vector((origin[0] + x_range[0], origin[1]), (origin[0] + x_range[1], origin[1])))
    ax.add_component(vector((origin[0], origin[1] + y_range[0]), (origin[0], origin[1] + y_range[1])))
    return ax
