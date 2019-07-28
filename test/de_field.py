import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math


def y_slope(x, y):
    #fun = -x / y
    #fun = 1 - 1/(x + y)
    #fun = math.cos(x) - y
    #fun = x**2 + y**2
    fun = ((1 - x**2) * y - x) / y
    return x, y, (1, fun)


def at(params):
    return y_slope(**params)



points = hl.surface_region(at, params={}, a_range=(-2, 2), b_range=(-2, 2), density=10, a_name='x', b_name='y')

scene = hl.slope_field(points, arrow_length=0.1, arrow_head_length=0.02)

scene.render_scene(x_range=(-3, 3), y_range=(-3, 3), resolution=300, density=150, background=hl.BLUE,
                   display=True, save=True, filename='de_field')
