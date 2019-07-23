import hallucinator
import numpy as np
import copy


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
            new_component.position = np.matmul(transformation, component.position)
            new_group.add_component(new_component)
        return new_group

    def rotate(self, theta, p=(0, 0)):
        return self.transform(hallucinator.rotate_about(theta, p))

    def translate(self, tx=0, ty=0):
        return self.transform(hallucinator.translate(tx, ty))

    def scale(self, sx=1, sy=1, p=(0, 0)):
        return self.transform(hallucinator.scale_about(sx, sy, p))

    def shear(self, sx=0, sy=0, p=(0, 0)):
        return self.transform(hallucinator.shear_about(sx, sy, p))

    def mirror(self, axis='x', offset=0):
        return self.transform(hallucinator.mirror_about(axis, offset))


class Group3(Group):
    def __init__(self, species='default'):
        Group.__init__(self, species)

    def transform(self, transformation):
        new_group = Group3()
        for component in self.components:
            new_component = copy.deepcopy(component)
            new_component.position = np.matmul(transformation, new_component.position)
            new_group.add_component(new_component)
        return new_group

    def rotate(self, theta, axis=(1, 0, 0), p=(0, 0, 0)):
        return self.transform(hallucinator.rotate_about_3(theta, axis, p))

    def translate(self, tx=0, ty=0, tz=0):
        return self.transform(hallucinator.translate_3(tx, ty, tz))

    def scale(self, sx=1, sy=1, sz=1, p=(0, 0, 0)):
        return self.transform(hallucinator.scale_about_3(sx, sy, sz, p))

    def shear(self):
        print('not implemented')

    def mirror(self, plane):
        print('not implemented')

    # TODO fix length
    def project(self, method='ortho', z_factor=0.05):
        new_group = Group(species=self.species + '_projected')
        for component in self.components:
            new_group.add_component(component.project(method=method, z_factor=z_factor))
        return new_group
