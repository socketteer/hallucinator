import ikonal
import numpy as np
import copy


# TODO individual density
class ParaObject:
    def __init__(self, f=None, path=(0, 1), length='auto', species='default'):
        self.f = f
        self.path = path
        self.position = ikonal.IDENTITY3
        self.species = species

        if length == 'auto':
            self.length = path[1] - path[0]
        else:
            self.length = length

    def at(self, p, debug=False):
        if debug:
            print(self.position)
            print(self.f(p))
        return np.matmul(self.position, self.f(p) + (1,))


class ParaObject3:
    def __init__(self, f=None, path=(0, 1), length='auto', species='default'):
        self.f = f
        self.path = path
        self.position = ikonal.IDENTITY4
        self.species = species

        if length == 'auto':
            self.length = path[1] - path[0]
        else:
            self.length = length

    def at(self, p, debug=False):
        if debug:
            print(self.position)
            print(self.f(p))
        return np.matmul(self.position, self.f(p) + (1,))

    def project(self, method='ortho'):
        new = ParaObject(f=lambda p: self.f(p),
                         path=self.path,
                         length=self.length,
                         species=self.species + '_projected')

        new_position = np.matmul(ikonal.ORTHO_PROJECT, self.position)
        new.position = np.delete(new_position, 2, axis=0)
        return new


class Group:
    def __init__(self, species='default'):
        self.components = []
        self.species = species

    def add_component(self, comp):
        self.components.append(comp)

    def transform(self, transformation):
        new_group = Group()
        for component in self.components:
            new_component = copy.deepcopy(component)
            new_component.position = np.matmul(component.position, transformation)
            new_group.add_component(new_component)
        return new_group

    def rotate(self, theta, p=(0, 0)):
        return self.transform(ikonal.rotate_about(theta, p))

    def translate(self, tx=0, ty=0):
        return self.transform(ikonal.translate(tx, ty))

    def scale(self, sx=1, sy=1, p=(0, 0)):
        return self.transform(ikonal.scale_about(sx, sy, p))

    def shear(self, sx=0, sy=0, p=(0, 0)):
        return self.transform(ikonal.shear_about(sx, sy, p))

    def mirror(self, axis='x', offset=0):
        return self.transform(ikonal.mirror_about(axis, offset))


class Group3(Group):
    def __init__(self, species='default'):
        Group.__init__(self, species)

    def transform(self, transformation):
        new_group = Group3()
        for component in self.components:
            new_component = copy.deepcopy(component)
            new_component.position = np.matmul(component.position, transformation)
            new_group.add_component(new_component)
        return new_group

    def rotate(self, theta, axis=(1, 0, 0)):
        return self.transform(ikonal.rotate_3(theta, axis))

    def translate(self, tx=0, ty=0, tz=0):
        return self.transform(ikonal.translate_3(tx, ty, tz))

    def scale(self, sx=1, sy=1, sz=1, p=(0, 0, 0)):
        return self.transform(ikonal.scale_about_3(sx, sy, sz, p))

    def shear(self):
        print('not implemented')

    def mirror(self, plane):
        print('not implemented')

    # TODO fix length
    def project(self, method='ortho'):
        new_group = Group(species=self.species + '_projected')
        for component in self.components:
            new_group.add_component(component.project(method=method))
        return new_group
