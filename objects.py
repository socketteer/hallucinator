import math


def line(m, b):
    return lambda x: [x, m*x + b]


def circle(r, c):
    return lambda theta: [r * math.cos(theta) + c[0], r * math.sin(theta) + c[1]]


