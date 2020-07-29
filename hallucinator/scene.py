import hallucinator as hl
import numpy as np
import copy


# TODO separate params for individual objects in groups?
# TODO random sampling

def obj_to_set(obj, params, region_type='path', density=5):
    if isinstance(obj, hl.Group):
        points = set()
        for component in obj.components:
            new_points = obj_to_set(component, params, region_type, density)
            if new_points:
                points = points.union(new_points)
        return points
    else:
        return obj.region(region_type)(at=obj.at, params=params, density=density)


def obj_to_lines(obj, params):
    if isinstance(obj, hl.Group):
        lines = set()
        for component in obj.components:
            new_lines = obj_to_lines(component, params)
            if new_lines:
                lines = lines.union(new_lines)
        return lines
    else:
        return hl.wireframe_lines(at=obj.at, params=params,
                                  **obj.region_params)


class Scene:
    def __init__(self):
        self.objects = {}

    # TODO auto naming
    def add_object(self, obj, name):
        self.objects[name] = obj
        return obj

    def frame_at_p(self, params,
                   camera_position='default',
                   projection_type='none',
                   region_params='none',
                   styles='uniform',
                   density=5):
        """
        :return: set of points { , gradient, or (R, G, B)}
        """

        # TODO global params

        if not camera_position == 'default':
            scene_position = np.linalg.inv(camera_position)
            return self.transform(scene_position).frame_at_p(params=params,
                                                             camera_position='default',
                                                             projection_type=projection_type,
                                                             region_params=region_params,
                                                             styles=styles,
                                                             density=density)

        if not projection_type == 'none':
            if projection_type == 'ortho':
                projection_matrix = hl.ORTHO_PROJECT
            elif projection_type == 'weak':
                # TODO x-factor param
                projection_matrix = hl.weak_project()
            else:
                print('invalid projection type')
                return
            return self.transform(projection_matrix).frame_at_p(params=params,
                                                                camera_position=camera_position,
                                                                projection_type='none',
                                                                region_params=region_params,
                                                                styles=styles,
                                                                density=density)
        lines = set()
        points = set()
        for name, obj in self.objects.items():
            # print('rendering {0}'.format(name))
            if name in params:
                param = params[name]
            else:
                param = {}
            region_type = obj.region_type

            if name in region_params:
                obj.region_params.update(region_params[name])

            # TODO fix all this
            if obj.region_type == "2d":
                if styles[name] == "uniform":
                    region_type = "surface"
                elif styles[name] == "wireframe":
                    region_type = "wireframe"
                elif styles[name] == "line":
                    region_type = "line"

            if region_type == "line":
                obj_lines = obj_to_lines(obj=obj, params=param)
                lines = lines.union(obj_lines)

            else:
                obj_points = obj_to_set(obj=obj, params=param, density=density, region_type=region_type)
                points = points.union(obj_points)

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

    #TODO use a master dictionary for all varying params
    def render_scene(self, params="none",
                     x_range=(-10, 10),
                     y_range=(-10, 10),
                     camera_position='default',
                     projection_type='none',
                     resolution=5,
                     density=5,
                     foreground=hl.WHITE,
                     background=hl.BLACK,
                     styles='uniform',
                     region_params="none",
                     display=False,
                     save=False,
                     filename='default',
                     backdrop="new"):
        # TODO default styles value
        if params == "none":
            params = {}
        # if style == "line":
        points, lines = self.frame_at_p(params=params,
                                        camera_position=camera_position,
                                        projection_type=projection_type,
                                        region_params=region_params,
                                        styles=styles,
                                        density=density)

        lines_arr = hl.lines_to_bichrome(lines=lines,
                                         x_range=x_range,
                                         y_range=y_range,
                                         foreground=foreground,
                                         background=background,
                                         resolution=resolution,
                                         backdrop=backdrop)
        arr = hl.set_to_bichrome(points=points,
                                 x_range=x_range,
                                 y_range=y_range,
                                 foreground=foreground,
                                 background=background,
                                 resolution=resolution,
                                 backdrop=lines_arr)

        if display:
            hl.render_from_array(arr)
        if save:
            hl.save_img(arr, filename)
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
