import hallucinator as hl
import numpy as np
import copy


class ParaObject:
    def __init__(self, f, region_type="path", region_params="none", species='default'):
        self.f = f
        self.region_type = region_type
        if region_params == "none":
            self.region_params = {}
        else:
            self.region_params = region_params
        self.species = species
        self.position = None

    def eval_at(self, p):
        return self.at({'p': p})

    def at(self, **params):
        """
        :param params:
        :return: (x, y, ( , gradient, or (R, G, B)))
        """
        there = self.f(**params)
        values = None
        if len(there) > self.position.shape[1] - 1:
            num_vals = len(there) + 1 - self.position.shape[0]
            values = there[-num_vals]
            there = there[:-num_vals]
        unnormalized_coordinates = np.matmul(self.position, there + (1,))
        normalized_coordinates = unnormalized_coordinates / unnormalized_coordinates[-1]
        # transformed = tuple(normalized_coordinates[:-1]) + (there[-1],)

        transformed = tuple(normalized_coordinates[:-1])
        return transformed + (values,)

    def transform(self, transformation):
        new_component = self.copy()
        new_component.position = np.matmul(transformation, new_component.position)
        return new_component

    # TODO does everything work right?
    def copy(self):
        return copy.deepcopy(self)

    def region(self, density):
        if self.region_type == 'path':
            sampler = hl.path_points(**self.region_params, density=density)
        elif self.region_type == '2d':
            sampler = hl.surface_points(**self.region_params, density=density)
        elif self.region_type == 'lattice':
            print('lattice')
            return
        else:
            print('error: invalid region type')
            return
        # print('sampler:', sampler)
        # print(type(sampler))
        # print('f sampler:', self.f(sampler))
        # print(type(self.f(sampler)))
        # print(self.f)
        return self.f(sampler)


class ParaObject2(ParaObject):
    def __init__(self, f, region_type="path", region_params="none", species='default'):
        ParaObject.__init__(self, f, region_type, region_params, species)
        self.position = hl.IDENTITY3

    def rotate(self, theta, p=(0, 0)):
        return self.transform(hl.rotate_about(theta, p))

    def translate(self, tx=0, ty=0):
        return self.transform(hl.translate(tx, ty))

    def scale(self, sx=1, sy=1, p=(0, 0)):
        return self.transform(hl.scale_about(sx, sy, p))

    def shear(self, sx=0, sy=0, p=(0, 0)):
        return self.transform(hl.shear_about(sx, sy, p))

    def mirror(self, axis='x', offset=0):
        return self.transform(hl.mirror_about(axis, offset))

    def add_disturbance(self, disturbance, init_pos, polarization):
        def f(p, t): return disturbance(p - init_pos, t) * np.asarray(polarization)

        self.f = lambda p, t: tuple(np.add(self.f(p, t), f(p, t)))


class ParaObject3(ParaObject):
    def __init__(self, f, region_type="path", region_params="none", species='default'):
        ParaObject.__init__(self, f, region_type, region_params, species)
        self.position = hl.IDENTITY4

    def project(self, method='ortho', z_factor=0.02):
        new = ParaObject2(f=self.f,
                          region_type=self.region_type,
                          region_params=self.region_params,
                          species=self.species + '_projected')

        if method == 'ortho':
            projection_matrix = hl.ORTHO_PROJECT
        elif method == 'weak':
            projection_matrix = hl.weak_project(z_factor)
        else:
            projection_matrix = hl.ORTHO_PROJECT

        new_position = np.matmul(projection_matrix, self.position)
        new.position = np.delete(new_position, 2, axis=0)
        return new

    def rotate(self, theta, axis=(1, 0, 0), p=(0, 0, 0)):
        return self.transform(hl.rotate_about_3(theta, axis, p))

    def translate(self, t):
        return self.transform(hl.translate_3(t))

    def scale(self, sx=1, sy=1, sz=1, p=(0, 0, 0)):
        return self.transform(hl.scale_about_3(sx, sy, sz, p))

    def shear(self, xy=0, xz=0, yx=0, yz=0, zx=0, zy=0, p=(0, 0, 0)):
        return self.transform(hl.shear_about_3(xy, xz, yx, yz, zx, zy, p))

    def mirror(self, plane):
        print('not implemented')

    # TODO only good for surfaces
    # TODO combine these two functions into one
    # only works if there is not already a disturbance
    def add_disturbance(self, disturbance, init_pos, polarization, start_time=0):
        def f(a, b, t): return 0 if t - start_time < 0 else (disturbance(a - init_pos[0],
                                                                         b - init_pos[1],
                                                                         t - start_time)
                                                             * np.asarray(polarization))

        copy_of_f = copy.copy(self.f)
        self.f = lambda a, b, t: tuple(np.add(f(a, b, t), copy_of_f(a, b)))

    # only works if there is already a time dependent disturbance
    def add_more_disturbances(self, disturbance, init_pos, polarization, start_time=0):
        def f(a, b, t): return 0 if t - start_time < 0 else (disturbance(a - init_pos[0], b - init_pos[1], t-start_time)
                                * np.asarray(polarization))

        copy_of_f = copy.copy(self.f)
        self.f = lambda a, b, t: tuple(np.add(f(a, b, t), copy_of_f(a, b, t)))
