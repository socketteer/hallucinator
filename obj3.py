import math
import group


'''parametric functions'''


def line(p0, dx, dy, dz):
    return lambda p: (p0[0] + p*dx, p0[1] + p*dy, p0[2] + p*dz)


'''object primitives'''


def vector(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x_len = x2 - x1
    y_len = y2 - y1
    z_len = z2 - z1
    distance = math.sqrt(x_len**2 + y_len**2 + z_len**2)
    return group.ParaObject(line(p1, x_len/distance, y_len/distance, z_len/distance),
                            path=(0, distance),
                            num_points=distance)


'''groups'''


def box(h, w, d, p0):
    box = group.Group()
    box.add_component(vector(p0, (p0[0]+h, p0[1], p0[2])))
    box.add_component(vector(p0, (p0[0], p0[1]+w, p0[2])))
    box.add_component(vector(p0, (p0[0], p0[1], p0[2]+d)))
    box.add_component(vector((p0[0]+h, p0[1], p0[2]), (p0[0]+h, p0[1]+w, p0[2])))
    box.add_component(vector((p0[0]+h, p0[1], p0[2]), (p0[0]+h, p0[1], p0[2]+d)))
    box.add_component(vector((p0[0], p0[1]+w, p0[2]), (p0[0]+h, p0[1]+w, p0[2])))
    box.add_component(vector((p0[0], p0[1]+w, p0[2]), (p0[0], p0[1]+w, p0[2]+d)))
    box.add_component(vector((p0[0], p0[1], p0[2]+d), (p0[0]+h, p0[1], p0[2]+d)))
    box.add_component(vector((p0[0], p0[1], p0[2]+d), (p0[0], p0[1]+w, p0[2]+d)))
    box.add_component(vector((p0[0]+h, p0[1]+w, p0[2]+d), (p0[0]+h, p0[1]+w, p0[2])))
    box.add_component(vector((p0[0]+h, p0[1]+w, p0[2]+d), (p0[0]+h, p0[1], p0[2]+d)))
    box.add_component(vector((p0[0]+h, p0[1]+w, p0[2]+d), (p0[0], p0[1]+w, p0[2]+d)))
    return box
