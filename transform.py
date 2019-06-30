import math
import group


def transform(operator, operand):
    if isinstance(operand, group.Group):
        new = group.Group()
        for component in operand.components:
            new.add_component(transform(operator, component))
        return new
    elif isinstance(operand, group.ParaObject):
        return group.ParaObject(lambda x: operator(operand.func(x)), operand.path, operand.num_points)
    elif isinstance(operand, function):
        return lambda x: operator(operand(x))


'''transformation lambdas'''


def rotate_deg(theta, p=(0, 0)):
    return rotate(math.radians(theta), p)


def rotate(theta, p=(0, 0)):
    if p == (0, 0):
        return lambda xy: (xy[0] * math.cos(theta) - xy[1] * math.sin(theta),
                           xy[1] * math.cos(theta) + xy[0] * math.sin(theta))
    else:
        mv_org = translate(-p[0], -p[1])
        rot_org = lambda xy: rotate(theta, (0, 0))(mv_org(xy))
        mv_back = lambda xy: translate(p[0], p[1])(rot_org(xy))
        return mv_back


def translate(x, y):
    return lambda xy: (xy[0] + x, xy[1] + y)


'''3d transforms'''


def rotate_deg_3(theta, axis='X'):
    return rotate_3(math.radians(theta), axis)


def rotate_3(theta, axis='X'):
    if axis == 'Z':
        return lambda xyz: (xyz[0] * math.cos(theta) - xyz[1] * math.sin(theta),
                            xyz[0] * math.sin(theta) + xyz[1] * math.cos(theta),
                            xyz[2])
    elif axis == 'X':
        return lambda xyz: (xyz[0],
                            xyz[1] * math.cos(theta) - xyz[2] * math.sin(theta),
                            xyz[1] * math.sin(theta) + xyz[2] * math.cos(theta))
    elif axis == 'Y':
        return lambda xyz: (xyz[0] * math.cos(theta) - xyz[2] * math.sin(theta),
                            xyz[1],
                            xyz[0] * math.sin(theta) + xyz[2] * math.cos(theta))
    else:
        print('invalid axis')


def translate_3(x, y, z):
    return lambda xyz: (xyz[0] + x, xyz[1] + y, xyz[2] + z)


def weak_project(pov=(0, 0, 0), z_scale=0.005):
    """
    :param pov:
    :param z_scale:
    :return:
    returns an operator which projects a three dimensional
    set of points onto a two dimensional
    canvas depicting a view from a point located at [pov]
    pointing in the positive z direction"""

    return lambda xyz: ((xyz[0] - pov[0])/((xyz[2] - pov[2]) * z_scale),
                        (xyz[1] - pov[1])/((xyz[2] - pov[2]) * z_scale))
