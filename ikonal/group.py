import ikonal
import numpy as np


#TODO individual density
#TODO 3d transforms
#TODO separate class for 3d to avoid stupid
class ParaObject:
    def __init__(self, f, path, length='auto', species='default'):
        self.f = lambda p: (f(p)[0], f(p)[1], 1)
        self.path = path
        self.position = ikonal.IDENTITY3
        if length == 'auto':
            self.length = path[1] - path[0]
        else:
            self.length = length
        self.species = species

    def rotate(self, theta, p=(0, 0)):
        return ikonal.transform(ikonal.rotate_about(theta, p), self)

    def translate(self, x=0, y=0):
        return ikonal.transform(ikonal.translate(x, y), self)

    #TODO recalculate density
    def scale(self, x=1, y=1, p=(0, 0)):
        return ikonal.transform(ikonal.scale_about(x, y, p), self)

    def at(self, p):
        return np.matmul(self.position, self.f(p))


'''class ParaObject3:
    def __init__(self, f, path, length='auto', species='default'):
        self.f = lambda p: (f(p)[0], f(p)[1], f(p)[3], 1)
        self.path = path
        self.position = ikonal.IDENTITY4
        if length == 'auto':
            self.length = path[1] - path[0]
        else:
            self.length = length
        self.species = species

    def rotate(self, theta, p=(0, 0)):
        return ikonal.transform(ikonal.rotate_about_3(theta, p), self)

    def translate(self, x, y):
        return ikonal.transform(ikonal.translate_3(x, y), self)

    #TODO recalculate density
    def scale(self, x, y, p=(0, 0)):
        return ikonal.transform(ikonal.scale_about_3(x, y, p), self)

    def at(self, p):
        return np.matmul(self.position, self.f(p))'''


class Group:
    def __init__(self, species='default'):
        self.components = []
        self.species = species

    def add_component(self, comp):
        self.components.append(comp)

    def rotate(self, theta, p=(0, 0)):
        new_group = Group(species=self.species)
        for component in self.components:
            new_group.add_component(component.rotate(theta, p))
        return new_group

    def translate(self, x=0, y=0):
        new_group = Group(species=self.species)

        for component in self.components:
            new_group.add_component(component.translate(x, y))
        return new_group

    def scale(self, x=1, y=1, p=(0, 0)):
        new_group = Group(species=self.species)

        for component in self.components:
            new_group.add_component(component.scale(x, y, p))
        return new_group

