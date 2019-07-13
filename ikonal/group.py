import ikonal


#TODO individual density
class ParaObject:
    def __init__(self, func, path, length='auto', dim=2, species='default'):
        self.func = func
        self.path = path
        if length == 'auto':
            self.length = path[1] - path[0]
        else:
            self.length = length
        self.dim = dim
        self.species = species

    def rotate(self, theta, p=(0, 0), axis='X'):
        if self.dim == 2:
            return ikonal.transform(ikonal.rotate_deg(theta, p), self)
        else:
            return ikonal.transform(ikonal.rotate_deg_3(theta, axis), self)

    def translate(self, x, y, z='none'):
        if self.dim == 2:
            return ikonal.transform(ikonal.translate(x, y), self)
        else:
            return ikonal.transform(ikonal.translate_3(x, y, z), self)


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
            return ikonal.transform(ikonal.rotate_deg(theta, p), self)
        else:
            return ikonal.transform(ikonal.rotate_deg_3(theta, axis), self)

    def translate(self, x, y, z='none'):
        if self.dim == 2:
            return ikonal.transform(ikonal.translate(x, y), self)
        else:
            return ikonal.transform(ikonal.translate_3(x, y, z), self)

