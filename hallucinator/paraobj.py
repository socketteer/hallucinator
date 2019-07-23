import hallucinator
import numpy as np
import copy


# TODO individual density
class ParaObject:
    def __init__(self, f, region, species='default'):
        self.f = f
        self.region = region
        self.species = species
        self.position = None

    def eval_at(self, p):
        return self.at({'p': p})

    def at(self, params):
        """
        :param params:
        :return: (x, y, ( , gradient, or (R, G, B)))
        """
        there = self.f(**params)
        unnormalized_coordinates = np.matmul(self.position, there + (1,))
        normalized_coordinates = unnormalized_coordinates / unnormalized_coordinates[-1]
        transformed = tuple(normalized_coordinates[:-1]) + (there[-1],)
        return transformed

    def transform(self, transformation):
        new_component = copy.deepcopy(self)
        new_component.position = np.matmul(transformation, new_component.position)
        return new_component


class ParaObject2(ParaObject):
    def __init__(self, f, region, species='default'):
        ParaObject.__init__(self, f, region, species)
        self.position = hallucinator.IDENTITY3

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


class ParaObject3(ParaObject):
    def __init__(self, f, region,  species='default'):
        ParaObject.__init__(self, f, region, species)
        self.position = hallucinator.IDENTITY4

    def project(self, method='ortho', z_factor=0.05):
        new = ParaObject(f=self.f,
                         region=self.region,
                         species=self.species + '_projected')

        if method == 'ortho':
            projection_matrix = hallucinator.ORTHO_PROJECT
        elif method == 'weak':
            projection_matrix = hallucinator.weak_project(z_factor)
        else:
            projection_matrix = hallucinator.ORTHO_PROJECT

        new_position = np.matmul(projection_matrix, self.position)
        new.position = np.delete(new_position, 2, axis=0)
        return new

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
