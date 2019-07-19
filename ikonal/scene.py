import ikonal


def frame_at_p(scene, params, density=5):
    """
    :param scene:
    :param params:
    :param density:
    :return: set of points { , gradient, or (R, G, B)}
    """

    points = set()
    #TODO global params
    for name, obj in scene.objects.items():
        if name in params:
            param = params[name]
        else:
            param = {}
        obj_points = ikonal.obj_to_set(obj=obj, params=param, density=density)
        points = points.union(obj_points)
    return points


class Scene:
    def __init__(self):
        self.objects = {}

    #TODO auto naming
    def add_object(self, obj, name):
        self.objects[name] = obj


class MonochromeScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def render_scene(self, params="none",
                     x_range=(-10, 10),
                     y_range=(-10, 10),
                     resolution=5,
                     density=5,
                     foreground=ikonal.WHITE,
                     background=ikonal.BLACK,
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
        :param display:
        :param save:
        :param filename:
        :param backdrop:
        :return:
        """
        if params=="none":
            params={}
        points = frame_at_p(self, params, density)
        arr = ikonal.set_to_bichrome(points=points,
                                     x_range=x_range,
                                     y_range=y_range,
                                     foreground=foreground,
                                     background=background,
                                     resolution=resolution,
                                     backdrop=backdrop)
        if display:
            ikonal.render_from_array(arr)
        if save:
            ikonal.save_img(arr, filename)
        return arr


class GrayscaleScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def render_scene(self, params="none",
                     x_range=(-10, 10),
                     y_range=(-10, 10),
                     resolution=5,
                     density=5,
                     black_ref=-1.0,
                     white_ref=1.0,
                     default=ikonal.BLUE,
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
        :param black_ref:
        :param white_ref:
        :param default:
        :param display:
        :param save:
        :param filename:
        :param backdrop:
        :return:
        """
        if params=="none":
            params={}
        points = frame_at_p(self, params, density)
        arr = ikonal.set_to_gradient(points=points,
                                     x_range=x_range,
                                     y_range=y_range,
                                     black_ref=black_ref,
                                     white_ref=white_ref,
                                     default=default,
                                     resolution=resolution,
                                     backdrop=backdrop)
        if display:
            ikonal.render_from_array(arr)
        if save:
            ikonal.save_img(arr, filename)
        return arr


class ColorScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def render_scene(self):
        pass
