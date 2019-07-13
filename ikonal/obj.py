import math
import ikonal

'''parametric functions'''


def line(p0, dx, dy):
    return lambda p: (p0[0] + p * dx, p0[1] + p * dy)


def circle_p(r, c):
    return lambda theta: (r * math.cos(theta) + c[0], r * math.sin(theta) + c[1])


def wave(a, f, p):
    return lambda t: (t, a * math.sin(2 * math.pi * f * t + p))


'''object primitives'''


def vector(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    distance = math.hypot(x_len, y_len)
    return ikonal.ParaObject(line(p1, x_len / distance, y_len / distance),
                             path=(0, distance),
                             length=distance,
                             species='vector')


def circle(r, c):
    return ikonal.ParaObject(circle_p(r, c),
                             path=(0, 2 * math.pi),
                             length=2 * math.pi * r,
                             species='circle')


'''groups'''


def rectangle(h, w, p0):
    rect = ikonal.Group(species='rectangle')
    rect.add_component(vector((p0[0], p0[1]), (p0[0], p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1]), (p0[0] + w, p0[1])))
    rect.add_component(vector((p0[0] + w, p0[1]), (p0[0] + w, p0[1] + h)))
    rect.add_component(vector((p0[0], p0[1] + h), (p0[0] + w, p0[1] + h)))
    return rect


def square(w, p0):
    return rectangle(w, w, p0)


def axes(x_range, y_range, origin=(0, 0)):
    ax = ikonal.Group(species='axes')
    ax.add_component(vector((origin[0] + x_range[0], origin[1]), (origin[0] + x_range[1], origin[1])))
    ax.add_component(vector((origin[0], origin[1] + y_range[0]), (origin[0], origin[1] + y_range[1])))
    return ax
