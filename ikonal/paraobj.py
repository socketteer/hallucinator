import ikonal
import numpy as np
import copy


# TODO individual density
class ParaObject:
    def __init__(self, f, region, species='default'):
        self.f = f
        self.region = region
        self.position = ikonal.IDENTITY3
        self.species = species

    def eval_at(self, p):
        return self.at({'p': p})

    def at(self, params):
        """
        :param params:
        :return: (x, y, ( , gradient, or (R, G, B)))
        """
        there = self.f(**params)
        transformed = tuple(np.matmul(self.position, there[:-1] + (1,))[:-1]) + (there[-1],)
        return transformed

    def transform(self, transformation):
        new_component = copy.deepcopy(self)
        new_component.position = np.matmul(transformation, new_component.position)
        return new_component

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


class ParaObject3:
    def __init__(self, f, region,  species='default'):
        self.f = f
        self.region = region
        self.position = ikonal.IDENTITY4
        self.species = species

    def eval_at(self, p):
        return self.at({'p': p})

    def at(self, params):
        """
        :param p:
        :return: (x, y, z, ( , gradient, or (R, G, B)))
        """
        there = self.f(**params)
        transformed = tuple(np.matmul(self.position, there[:-1] + (1,))[:-1]) + (there[-1],)
        return transformed

    def project(self, method='ortho'):
        new = ParaObject(f=lambda p: self.f(p),
                         region=self.region,
                         species=self.species + '_projected')

        new_position = np.matmul(ikonal.ORTHO_PROJECT, self.position)
        new.position = np.delete(new_position, 2, axis=0)
        return new

    def transform(self, transformation):
        new_component = copy.deepcopy(self)
        new_component.position = np.matmul(transformation, new_component.position)
        return new_component

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
