import render
import discretizer
import transform
import simulate


def frame_to_image(frame, x_range=(-10, 10), y_range=(-10, 10),
                   foreground=render.WHITE, background=render.BLACK,
                   resolution=50):
    points = set()
    for obj in frame.objects:
        print('rendering ', obj.species)
        points = points.union(discretizer.obj_to_set(obj, resolution))
    return render.set_to_bichrome(points,
                                  x_range=tuple(i * resolution for i in x_range),
                                  y_range=tuple(i * resolution for i in y_range),
                                  foreground=foreground, background=background)


class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, object):
        self.objects.append(object)

    def discr_render(self, x_range=(-10, 10), y_range=(-10, 10),
                     resolution=50,
                     foreground=render.WHITE, background=render.BLACK,
                     display=True,
                     save=False, filename='default'):
        arr = frame_to_image(self, x_range, y_range, foreground, background, resolution)
        if display:
            render.render_from_array(arr)
        if save:
            render.save_img(arr, filename)
        return arr


class Scene3(Scene):
    def discr_render(self, x_range=(-1000, 1000), y_range=(-1000, 1000),
                     pov=(0, 0, 0), z_scale=0.005, method="weak",
                     foreground=render.WHITE, background=render.BLACK,
                     display=True,
                     save=False, filename='default'):
        points = set()
        for obj in self.objects:
            points = points.union(discretizer.obj_to_set(obj))
        points = render.project(points, pov=pov, z_scale=z_scale, method=method)
        arr = render.set_to_bichrome(points, x_range=x_range, y_range=y_range,
                                     foreground=foreground, background=background)
        if display:
            render.render_from_array(arr)
        if save:
            render.save_img(arr, filename)
        return arr

    def lazy_render(self, x_range=(-1000, 1000), y_range=(-1000, 1000),
                    pov=(0, 0, 0), z_scale=0.005,
                    foreground=render.WHITE,
                    background=render.BLACK, display=True, save=False,
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
        for obj in self.objects:
            projected.add_object(transform.transform(transform.weak_project(pov, z_scale), obj))
        return projected.discr_render(x_range, y_range, foreground, background, display, save, filename)
