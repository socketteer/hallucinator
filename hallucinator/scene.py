import hallucinator as hl
import numpy as np
import copy


# TODO separate params for individual objects in groups?
# TODO random sampling

# def obj_to_set(obj, region_type='path', density=5, **render_params):
#     if isinstance(obj, hl.Group):
#         points = set()
#         for component in obj.components:
#             new_points = obj_to_set(component, region_type, density, **render_params)
#             if new_points:
#                 points = points.union(new_points)
#         return points
#     else:
#         #return obj.region(region_type)(at=obj.at, density=density, **render_params)
#         return obj.region(region_type, **render_params)


def obj_to_lines(obj, params):
    if isinstance(obj, hl.Group):
        lines = set()
        for component in obj.components:
            new_lines = obj_to_lines(component, params)
            if new_lines:
                lines = lines.union(new_lines)
        return lines
    else:
        return hl.wireframe_lines(at=obj.at, params=params, **obj.region_params)


class Scene:
    def __init__(self):
        self.objects = {}

    # TODO auto naming
    def add_object(self, obj, name):
        self.objects[name] = obj
        return obj

    def frame(self,
              camera_position=(0, 0, 0),
              projection_type='weak',
              styles='uniform',
              **render_params):
        points = []
        scene_position = np.matmul(hl.translate_3(tuple(i*-1 for i in camera_position)), hl.IDENTITY4)

        if projection_type == 'ortho':
            projection_matrix = hl.ORTHO_PROJECT
        elif projection_type == 'weak':
            projection_matrix = hl.weak_project()
        else:  # no projection
            projection_matrix = hl.IDENTITY4

        transform = np.matmul(projection_matrix, scene_position)

        # this draws all points in scene at once
        # TODO separate render types
        for obj in self.objects.values():
            obj_points = obj.region(styles, **render_params)

            ones = np.ones(obj_points.shape[1])

            obj_points = np.vstack((obj_points, ones))
            transformed_obj_points = np.matmul(obj.position, obj_points)
            points.append(transformed_obj_points)

        points = np.array(points)
        points = points.reshape((4, points.shape[0] * points.shape[2]))
        transformed_points = np.matmul(transform, points)
        normalized_points = np.divide(transformed_points, transformed_points[-1])
        transposed_points = normalized_points.transpose()

        return transposed_points

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
                     projection_type='none',
                     resolution=5,
                     foreground=hl.WHITE,
                     background=hl.BLACK,
                     styles='uniform',
                     backdrop="new",
                     **render_params):
        # TODO default styles value
        # if style == "line":
        points = self.frame(camera_position=camera_position,
                            projection_type=projection_type,
                            styles=styles,
                            **render_params)

        '''lines_arr = hl.lines_to_bichrome(lines=lines,
                                         x_range=x_range,
                                         y_range=y_range,
                                         foreground=foreground,
                                         background=background,
                                         resolution=resolution,
                                         backdrop=backdrop)'''
        # would this be faster with np arrays?
        arr = hl.points_to_bichrome(points=points,
                                    x_range=x_range,
                                    y_range=y_range,
                                    foreground=foreground,
                                    background=background,
                                    resolution=resolution)
        return arr

    def transform(self, transformation):
        new_scene = MonochromeScene()
        for name, obj in self.objects.items():
            #print(obj.position)
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
