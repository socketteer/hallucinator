import render
import discretizer


class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, object):
        self.objects.append(object)

    def render(self, x_range=(-1000, 1000), y_range=(-1000, 1000),
               foreground=render.WHITE, background=render.BLACK,
               display=True,
               save=False, filename='default'):
        points = set()
        for object in self.objects:
            points = points.union(discretizer.obj_to_set(object))
        arr = render.set_to_bichrome(points, x_range=x_range, y_range=y_range,
                                     foreground=foreground, background=background)
        if display:
            render.render_from_array(arr)
        if save:
            render.save_img(arr, filename)


class Scene3(Scene):
    def render(self, x_range=(-1000, 1000), y_range=(-1000, 1000),
               pov=(0, 0, 0), z_scale=0.005, method="weak",
               foreground=render.WHITE, background=render.BLACK,
               display=True,
               save=False, filename='default'):
        points = set()
        for object in self.objects:
            points = points.union(discretizer.obj_to_set(object))
        points = render.project(points, pov=pov, z_scale=z_scale, method=method)
        arr = render.set_to_bichrome(points, x_range=x_range, y_range=y_range,
                                     foreground=foreground, background=background)
        if display:
            render.render_from_array(arr)
        if save:
            render.save_img(arr, filename)
