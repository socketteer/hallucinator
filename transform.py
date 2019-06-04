import numpy as np
import math
import objects


def transform(operator, operand):
    if isinstance(operand, objects.Group):
        new = objects.Group()
        for component in operand.components:
            new.add_component(transform(operator, component))
        return new
    elif isinstance(operand, objects.ParaObject):
        return objects.ParaObject(lambda x: operator(operand.func(x)), operand.path, operand.num_points)
    elif isinstance(operand, function):
        return lambda x: operator(operand(x))


'''transformation lambdas'''


def rotate_deg(theta, p=(0, 0)):
    return rotate(math.radians(theta), p)


def rotate(theta, p=(0, 0)):
    if p == (0, 0):
        print(theta)
        return lambda xy: (xy[0] * math.cos(theta) - xy[1] * math.sin(theta),
                           xy[1] * math.cos(theta) + xy[0] * math.sin(theta))
    else:
        mv_org = translate(-p[0], -p[1])
        rot_org = lambda xy: rotate(theta, (0, 0))(mv_org(xy))
        mv_back = lambda xy: translate(p[0], p[1])(rot_org(xy))
        return mv_back


def translate(x, y):
    return lambda xy: (xy[0] + x, xy[1] + y)

