import math


class ParaObject:
    def __init__(self, func, path, num_points):
        self.func = func
        self.path = path
        self.num_points = num_points


class Group:
    def __init__(self):
        self.components = []

    def add_component(self, comp):
        self.components.append(comp)


'''parametric functions'''


def line(m, b):
    return lambda p: (p, m*p + b)


def ray(theta, d):
    return lambda p: (math.cos(theta)*p + d[0], math.sin(theta)*p + d[1])


def circle_p(r, c):
    return lambda theta: (r * math.cos(theta) + c[0], r * math.sin(theta) + c[1])


'''object primitives'''


def vector(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    distance = math.hypot(x_len, y_len)
    theta = math.atan2(y_len, x_len)
    return ParaObject(ray(theta, p1), [0, distance], distance)


def circle(r, c):
    return ParaObject(circle_p(r, c), [0, 2 * math.pi], 2 * math.pi * r)


'''groups'''


def rectangle(h, w, d):
    rect = Group()
    rect.add_component(vector([d[0], d[1]], [d[0], d[1]+h]))
    rect.add_component(vector([d[0], d[1]], [d[0]+w, d[1]]))
    rect.add_component(vector([d[0]+w, d[1]], [d[0]+w, d[1]+h]))
    rect.add_component(vector([d[0], d[1]+h], [d[0]+w, d[1]+h]))
    return rect


def square(w, d):
    return rectangle(w, w, d)


