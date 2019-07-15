import ikonal


def frame_to_image(frame, x_range=(-10, 10), y_range=(-10, 10),
                   foreground=ikonal.WHITE, background=ikonal.BLACK,
                   density=5, resolution=5, backdrop="new"):
    points = set()
    #print(frame.objects.values())
    for obj in frame.objects.values():
        points = points.union(ikonal.obj_to_set(obj=obj, density=density))
    return ikonal.set_to_bichrome(points,
                                  x_range=x_range,
                                  y_range=y_range,
                                  foreground=foreground,
                                  background=background,
                                  resolution=resolution,
                                  backdrop=backdrop)


class Scene:
    def __init__(self):
        self.objects = {}

    #TODO auto naming
    def add_object(self, obj, name):
        self.objects[name] = obj

    def render_scene(self, x_range=(-10, 10),
                     y_range=(-10, 10),
                     resolution=5,
                     density=5,
                     foreground=ikonal.WHITE,
                     background=ikonal.BLACK,
                     display=True,
                     save=False,
                     filename='default'):
        arr = frame_to_image(self, x_range, y_range, foreground, background, density, resolution)
        if display:
            ikonal.render_from_array(arr)
        if save:
            ikonal.save_img(arr, filename)
        return arr

#TODO get rid of this
class Scene3(Scene):
    def discr_render(self, x_range=(-1000, 1000), y_range=(-1000, 1000),
                     pov=(0, 0, 0), z_scale=0.005, method="weak",
                     foreground=ikonal.WHITE, background=ikonal.BLACK,
                     display=True,
                     save=False, filename='default'):
        points = set()
        for obj in self.objects.values():
            points = points.union(ikonal.obj_to_set(obj))
        points = ikonal.project(points, pov=pov, z_scale=z_scale, method=method)
        arr = ikonal.set_to_bichrome(points, x_range=x_range, y_range=y_range,
                                     foreground=foreground, background=background)
        if display:
            ikonal.render_from_array(arr)
        if save:
            ikonal.save_img(arr, filename)
        return arr

    def lazy_render(self, x_range=(-1000, 1000), y_range=(-1000, 1000),
                    pov=(0, 0, 0), z_scale=0.005,
                    foreground=ikonal.WHITE,
                    background=ikonal.BLACK, display=True, save=False,
                    filename='default'):
        """

        :param x_range:
        :param y_range:
        :param pov:
        :param z_scale:
        :param foreground:
        :param background:
        :param display:
        :param save:
        :param filename:
        :return:
        """
        projected = Scene()
        for obj in self.objects.values():
            projected.add_object(ikonal.transform(ikonal.weak_project(pov, z_scale), obj))
        return projected.discr_render(x_range, y_range, foreground, background, display, save, filename)
