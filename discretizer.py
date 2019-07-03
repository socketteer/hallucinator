import numpy as np
import group


#TODO evaluate 2d parametric surface in 3 dimensions
def para_to_array(x_min, x_max, y_min, y_max, func, path,
                  num_points="default", resolution=50):
    if np.ndim(path) == 1:
        if num_points == "default":
            num_points = path[1] - path[0];
        arr = np.zeros((x_max - x_min, y_max - y_min), dtype=np.bool)
        for i in np.linspace(path[0], path[1], num_points):
            x, y = np.rint(func(i)).astype(int)
            if x_min <= x < x_max and y_min <= y < y_max:
                arr[x-x_min, y-y_min] = 1
        return arr
    elif np.ndim(path) == 2:
        #TODO resolution
        if num_points == "default":
            pts_horiz = path[0][1] - path[0][0]
            pts_vert = path[1][1] - path[1][0]
        else:
            pts_horiz = num_points[0]
            pts_vert = num_points[1]

        arr = np.zeros((x_max - x_min, y_max - y_min), dtype=np.bool)
        for i in np.linspace(path[0][0], path[0][1], pts_horiz):
            for j in np.linspace(path[1][0], path[1][1], pts_vert):
                x, y = np.rint(func(i, j)).astype(int)
                if x_min <= x < x_max and y_min <= y < y_max:
                    arr[x-x_min, y-y_min] = 1
        return arr


def obj_to_set(obj, resolution=50):
    if isinstance(obj, group.Group):
        points = set()
        for component in obj.components:
            points = points.union(obj_to_set(component))
        return points
    elif isinstance(obj, group.ParaObject):
        return para_to_set(obj.func, obj.path, obj.num_points, resolution)


def para_to_set(func, path, num_points="default", resolution=50):
    if num_points == "default":
        num_points = path[1] - path[0]
    points = set()
    for i in np.linspace(path[0], path[1], num_points):
        points.add(tuple(np.rint(tuple(i * resolution for i in func(i))).astype(int)))
    return points


#TODO para surface

