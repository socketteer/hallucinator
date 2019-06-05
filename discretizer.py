import numpy as np
import group


def para_to_array(x_min, x_max, y_min, y_max, func, path, num_points="default"):
    if num_points == "default":
        num_points = path[1] - path[0];
    arr = np.zeros((x_max - x_min, y_max - y_min), dtype=np.bool)
    for i in np.linspace(path[0], path[1], num_points):
        x, y = np.rint(func(i)).astype(int)
        if x_min <= x < x_max and y_min <= y < y_max:
            arr[x-x_min, y-y_min] = 1
    return arr


def obj_to_set(obj):
    if isinstance(obj, group.Group):
        points = set()
        for component in obj.components:
            points = points.union(obj_to_set(component))
        return points
    elif isinstance(obj, group.ParaObject):
        return para_to_set(obj.func, obj.path, obj.num_points)


def para_to_set(func, path, num_points="default"):
    if num_points == "default":
        num_points = path[1] - path[0]
    points = set()
    for i in np.linspace(path[0], path[1], num_points):
        points.add(tuple(np.rint(func(i)).astype(int)))
    return points


#TODO para surface

