import hallucinator as hl
import numpy as np
import copy
from enum import Enum


# TODO separate params for individual objects in groups?
# TODO random sampling


class Styles(Enum):
    UNIFORM = "uniform"
    WIREFRAME = "wireframe"


class Projections(Enum):
    ORTHO = "ortho"
    WEAK = "weak"


#
# def obj_to_lines(obj, params):
#     if isinstance(obj, hl.Group):
#         lines = set()
#         for component in obj.components:
#             new_lines = obj_to_lines(component, params)
#             if new_lines:
#                 lines = lines.union(new_lines)
#         return lines
#     else:
#         return hl.wireframe_lines(at=obj.at, params=params, **obj.region_params)


class Scene:
    def __init__(self):
        self.objects = {}

    # TODO auto naming
    def add_object(self, obj, name):
        self.objects[name] = obj
        return obj

    def frame(self,
              camera_position=(0, 0, 0),
              projection_type=Projections.WEAK,
              styles=Styles.UNIFORM,
              densities=1):
        if not type(styles) == dict:
            styles_val = styles
            styles = {}
            for obj in self.objects:
                styles[obj] = styles_val

        if not type(densities) == dict:
            densities_val = densities
            densities = {}
            for obj in self.objects:
                densities[obj] = densities_val
        points = []
        lines = []
        endpoints1 = []
        endpoints2 = []
        scene_position = np.matmul(hl.translate_3(tuple(i * -1 for i in camera_position)), hl.IDENTITY4)

        if projection_type == Projections.ORTHO:
            projection_matrix = hl.ORTHO_PROJECT
        elif projection_type == Projections.WEAK:
            projection_matrix = hl.weak_project()
        else:  # no projection
            projection_matrix = hl.IDENTITY4

        transform = np.matmul(projection_matrix, scene_position)

        # TODO group objects
        for name, obj in self.objects.items():
            obj_points = obj.region(densities[name])
            if styles[name] == Styles.UNIFORM:
                obj_points = hl.reshape_array(obj_points)
                transformed_obj_points = np.matmul(obj.position, obj_points)
                if len(points) == 0:
                    points = transformed_obj_points
                else:
                    points = np.concatenate((points, transformed_obj_points), axis=1)
            elif styles[name] == Styles.WIREFRAME:
                # TODO 2d case
                if obj.region_type == 'path':
                    print('wireframe not implemented for path objects')
                    return
                h1 = obj_points[:, :, 1:]
                h2 = obj_points[:, :, :-1]
                v1 = obj_points[:, 1:, :]
                v2 = obj_points[:, :-1, :]
                h1 = hl.reshape_array(h1)
                h2 = hl.reshape_array(h2)
                v1 = hl.reshape_array(v1)
                v2 = hl.reshape_array(v2)

                new_endpoints1 = np.concatenate((h1, v1), axis=1)
                new_endpoints2 = np.concatenate((h2, v2), axis=1)
                new_endpoints1, new_endpoints2 = hl.apply_transforms(transforms=(obj.position, ),
                                                                     arrays=(new_endpoints1, new_endpoints2))

                if len(endpoints1) == 0:
                    endpoints1 = new_endpoints1
                    endpoints2 = new_endpoints2
                else:
                    endpoints1 = np.concatenate((endpoints1, new_endpoints1), axis=1)
                    endpoints2 = np.concatenate((endpoints2, new_endpoints2), axis=1)

        if len(endpoints1) > 0:
            endpoints1, endpoints2 = hl.apply_transforms((transform, ), (endpoints1, endpoints2))
            endpoints1 = np.divide(endpoints1, endpoints1[-1])
            endpoints2 = np.divide(endpoints2, endpoints2[-1])
            lines = np.array((endpoints1, endpoints2))
            lines = lines.transpose()
            lines = np.swapaxes(lines, 1, 2)
        if len(points) > 0:
            points = np.matmul(transform, points)
            points = np.divide(points, points[-1])
            points = points.transpose()

        return points, lines

    def transform(self, transformation):
        new_scene = Scene()
        for name, obj in self.objects.items():
            new_scene.add_object(obj.transform(transformation), name=name)
        return new_scene

    def copy(self):
        return copy.deepcopy(self)


class MonochromeScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def render_scene(self,
                     x_range=(-10, 10),
                     y_range=(-10, 10),
                     camera_position=(0, 0, 0),
                     projection_type=Projections.WEAK,
                     resolution=5,
                     foreground=hl.WHITE,
                     background=hl.BLACK,
                     styles=Styles.UNIFORM,
                     backdrop="new",
                     densities=1):

        points, lines = self.frame(camera_position=camera_position,
                                   projection_type=projection_type,
                                   styles=styles,
                                   densities=densities)
        if len(lines) > 0:
            lines_arr = hl.lines_to_bichrome(lines=lines,
                                             x_range=x_range,
                                             y_range=y_range,
                                             foreground=foreground,
                                             background=background,
                                             resolution=resolution,
                                             backdrop=backdrop)
        else:
            lines_arr = "new"
        arr = hl.points_to_bichrome(points=points,
                                    x_range=x_range,
                                    y_range=y_range,
                                    foreground=foreground,
                                    background=background,
                                    resolution=resolution,
                                    backdrop=lines_arr)
        return arr

    def transform(self, transformation):
        new_scene = MonochromeScene()
        for name, obj in self.objects.items():
            new_scene.add_object(obj.transform(transformation), name=name)
        return new_scene


# TODO update
class GrayscaleScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def render_scene(self, params="none",
                     x_range=(-10, 10),
                     y_range=(-10, 10),
                     camera_position='default',
                     projection_type='none',
                     resolution=5,
                     density=5,
                     black_ref=-1.0,
                     white_ref=1.0,
                     default=hl.BLUE,
                     style='uniform',
                     region_params="none",
                     display=False,
                     save=False,
                     filename='default',
                     backdrop="new"):
        if params == "none":
            params = {}

        points, _ = self.frame_at_p(params=params,
                                    camera_position=camera_position,
                                    projection_type=projection_type,
                                    region_params=region_params,
                                    style=style,
                                    density=density)
        arr = hl.set_to_gradient(points=points,
                                 x_range=x_range,
                                 y_range=y_range,
                                 black_ref=black_ref,
                                 white_ref=white_ref,
                                 default=default,
                                 resolution=resolution,
                                 backdrop=backdrop)
        if display:
            hl.render_from_array(arr)
        if save:
            hl.save_img(arr, filename)
        return arr


class ColorScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def render_scene(self):
        pass
