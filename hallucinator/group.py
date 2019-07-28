import hallucinator
import numpy as np
import copy


class Group:
    def __init__(self, region_type='path', species='default'):
        self.components = []
        self.region_type = region_type
        self.species = species

    def add_component(self, comp):
        self.components.append(comp)
        return comp

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

    def copy(self):
        return copy.deepcopy(self)


class Group3(Group):
    def __init__(self, region_type='path', species='default'):
        Group.__init__(self, region_type, species)

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

    def shear(self, xy=0, xz=0, yx=0, yz=0, zx=0, zy=0, p=(0, 0, 0)):
        return self.transform(hallucinator.shear_about_3(xy, xz, yx, yz, zx, zy, p))

    def mirror(self, plane):
        print('not implemented')

    # TODO fix length
    def project(self, method='ortho', z_factor=0.02):
        new_group = Group(species=self.species + '_projected')
        for component in self.components:
            new_group.add_component(component.project(method=method, z_factor=z_factor))
        return new_group
