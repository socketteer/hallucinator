import hallucinator as hl
import numpy as np
import copy


# TODO separate params for individual objects in groups?
# TODO random sampling

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
                   style='uniform',
                   density=5):
        """
        :param params:
        :param style:
        :param density:
        :return: set of points { , gradient, or (R, G, B)}
        """

        points = set()
        # TODO global params

        if not camera_position == 'default':
            scene_position = np.linalg.inv(camera_position)
            return self.transform(scene_position).frame_at_p(params=params,
                                                             camera_position='default',
                                                             projection_type=projection_type,
                                                             region_params=region_params,
                                                             style=style,
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
                                                                style=style,
                                                                density=density)

        for name, obj in self.objects.items():
            if name in params:
                param = params[name]
            else:
                param = {}
            region_type = obj.region_type

            if not region_params == "none":
                obj.region_params.update(region_params)

            if obj.region_type == "2d":
                if style == "uniform":
                    region_type = "surface"
                elif style == "wireframe":
                    region_type = "wireframe"

            # trans_obj = obj.transform(camera_position)

            obj_points = hl.obj_to_set(obj=obj, params=param, density=density, region_type=region_type)
            points = points.union(obj_points)
        return points

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

    def render_scene(self, params="none",
                     x_range=(-10, 10),
                     y_range=(-10, 10),
                     camera_position='default',
                     projection_type='none',
                     resolution=5,
                     density=5,
                     foreground=hl.WHITE,
                     background=hl.BLACK,
                     style='uniform',
                     region_params="none",
                     display=False,
                     save=False,
                     filename='default',
                     backdrop="new"):
        """

        :param params:
        :param x_range:
        :param y_range:
        :param resolution:
        :param density:
        :param foreground:
        :param background:
        :param style:
        :param region_params
        :param display:
        :param save:
        :param filename:
        :param backdrop:
        :return:
        """
        if params == "none":
            params = {}
        points = self.frame_at_p(params=params,
                                 camera_position=camera_position,
                                 projection_type=projection_type,
                                 region_params=region_params,
                                 style=style,
                                 density=density)
        arr = hl.set_to_bichrome(points=points,
                                 x_range=x_range,
                                 y_range=y_range,
                                 foreground=foreground,
                                 background=background,
                                 resolution=resolution,
                                 backdrop=backdrop)
        if display:
            hl.render_from_array(arr)
        if save:
            hl.save_img(arr, filename)
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
        """
        :param params:
        :param x_range:
        :param y_range:
        :param camera_position:
        :param projection_type:
        :param resolution:
        :param density:
        :param black_ref:
        :param white_ref:
        :param default:
        :param style:
        :param region_params:
        :param display:
        :param save:
        :param filename:
        :param backdrop:
        :return:
        """
        if params == "none":
            params = {}
        points = self.frame_at_p(params=params,
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
