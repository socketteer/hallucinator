import numpy as np
import ikonal


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
    if isinstance(obj, ikonal.Group):
        points = set()
        for component in obj.components:
            points = points.union(obj_to_set(component))
        return points
    elif isinstance(obj, ikonal.ParaObject):
        return para_to_set(obj.func, obj.path, obj.num_points, resolution)


def para_to_set(func, path, num_points="default", resolution=50):
    if num_points == "default":
        num_points = path[1] - path[0]
    points = set()
    for i in np.linspace(path[0], path[1], num_points):
        points.add(tuple(np.rint(tuple(u * resolution for u in func(i))).astype(int)))
    return points


def phasegrid(func, x_range, y_range, resolution=50):
    x_size = x_range[1] - x_range[0]
    y_size = y_range[1] - y_range[0]

    arr = np.zeros((x_size*resolution, y_size*resolution), dtype=np.float)

    i = 0
    j = 0
    for x in np.linspace(x_range[0], x_range[1], x_size*resolution):
        for y in np.linspace(y_range[0], y_range[1], y_size*resolution):
            #print('i', i)
            #print('j', j)
            #print('f({0},{1})'.format(x, y), func(x, y))
            arr[i][j] = func(x, y)
            #print(arr[i][j])
            j += 1
        j = 0
        i += 1
    return arr


#TODO para surface

