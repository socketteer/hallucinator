import math
import group


'''parametric functions'''


def line(p0, dx, dy):
    return lambda p: (p0[0] + p*dx, p0[1] + p*dy)


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
    return group.ParaObject(line(p1, x_len/distance, y_len/distance),
                            path=(0, distance),
                            num_points=distance)


def circle(r, c):
    return group.ParaObject(circle_p(r, c),
                            path=(0, 2 * math.pi),
                            num_points=2 * math.pi * r)


'''groups'''


def rectangle(h, w, p0):
    rect = group.Group()
    rect.add_component(vector([p0[0], p0[1]], [p0[0], p0[1]+h]))
    rect.add_component(vector([p0[0], p0[1]], [p0[0]+w, p0[1]]))
    rect.add_component(vector([p0[0]+w, p0[1]], [p0[0]+w, p0[1]+h]))
    rect.add_component(vector([p0[0], p0[1]+h], [p0[0]+w, p0[1]+h]))
    return rect


def square(w, p0):
    return rectangle(w, w, p0)


