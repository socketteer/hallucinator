import math
import ikonal
import operator
import numpy as np

'''parametric functions'''


def line_3(p0, dx, dy, dz):
    return lambda p: (p0[0] + p * dx, p0[1] + p * dy, p0[2] + p * dz, 1)


# TODO fix
def plane(p0, v1, v2):
    p0 = np.asarray(p0)
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)
    return lambda a, b: tuple(p0 + a * v1 + b * v2) + (1,)


'''object primitives'''


def vector_3(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    z_len = z2 - z1
    distance = math.sqrt(x_len ** 2 + y_len ** 2 + z_len ** 2)
    region = lambda at, params, density: ikonal.path_region(at=at,
                                                            params=params,
                                                            path_range=(0, distance),
                                                            path_length=distance,
                                                            density=density)
    return ikonal.ParaObject3(line_3(p1, x_len / distance, y_len / distance, z_len / distance),
                              region=region,
                              species='3vector')


def ellipse_3(h, w):
    pass


def plane_section(p0=(0, 0, 0), v1=(0, 1, 0), v2=(1, 0, 0), a_range=(0, 1), b_range=(0, 1)):
    a_length = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    b_length = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)
    region = lambda at, params, density: ikonal.rectangle_region(at=at,
                                                                 params=params,
                                                                 a_range=a_range,
                                                                 b_range=b_range,
                                                                 a_length=a_length,
                                                                 b_length=b_length,
                                                                 density=density)
    return ikonal.ParaObject3(plane(p0, v1, v2),
                              region=region,
                              species='plane')


'''groups'''


def rectangle_3(h, w):
    pass


def box(h, w, d, p0=(0, 0, 0)):
    b = ikonal.Group3(species='box')
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
    ax = ikonal.Group3(species='3axes')
    ax.add_component(vector_3((origin[0] + x_range[0], origin[1], origin[2]),
                              (origin[0] + x_range[1], origin[1], origin[2])))
    ax.add_component(vector_3((origin[0], origin[1] + y_range[0], origin[2]),
                              (origin[0], origin[1] + y_range[1], origin[2])))
    ax.add_component(vector_3((origin[0], origin[1], origin[2] + z_range[0]),
                              (origin[0], origin[1], origin[2] + z_range[1])))

    return ax
