import transform


class ParaObject:
    def __init__(self, func, path, num_points):
        self.func = func
        self.path = path
        self.num_points = num_points

    def rotate(self, theta, p=(0, 0)):
        return transform.transform(transform.rotate_deg(theta, p), self)

    def translate(self, x, y):
        return transform.transform(transform.translate(x, y), self)


class Group:
    def __init__(self):
        self.components = []

    def add_component(self, comp):
        self.components.append(comp)

    def rotate(self, theta, p=(0, 0)):
        return transform.transform(transform.rotate_deg(theta, p), self)

    def translate(self, x, y):
        return transform.transform(transform.translate(x, y), self)
