import transform


class ParaObject:
    def __init__(self, func, path, num_points, dim=2, species='default'):
        self.func = func
        self.path = path
        self.num_points = num_points
        self.dim = dim
        self.species = species

    def rotate(self, theta, p=(0, 0), axis='X'):
        if self.dim == 2:
            return transform.transform(transform.rotate_deg(theta, p), self)
        else:
            return transform.transform(transform.rotate_deg_3(theta, axis), self)

    def translate(self, x, y, z='none'):
        if self.dim == 2:
            return transform.transform(transform.translate(x, y), self)
        else:
            return transform.transform(transform.translate_3(x, y, z), self)


class Group:
    def __init__(self, dim=2, species='default'):
        self.components = []
        self.dim = dim
        self.type = type
        self.species = species

    def add_component(self, comp):
        self.components.append(comp)

    def rotate(self, theta, p=(0, 0), axis='X'):
        if self.dim == 2:
            return transform.transform(transform.rotate_deg(theta, p), self)
        else:
            return transform.transform(transform.rotate_deg_3(theta, axis), self)

    def translate(self, x, y, z='none'):
        if self.dim == 2:
            return transform.transform(transform.translate(x, y), self)
        else:
            return transform.transform(transform.translate_3(x, y, z), self)

