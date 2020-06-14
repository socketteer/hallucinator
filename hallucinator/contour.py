import math
from pprint import pprint

import cv2
import numpy as np
import numexpr as ne
import hallucinator as hl


# Ellipsoid 1 = x2/a2 + y2/b2 + z2/c2. (a,0,0), (0,b,0), (0,0,c) lie in the surface
def ellipsoid(xy, center=0, a=.5, b=1, **kwargs):
    x2y2 = ne.evaluate("(xy-center)**2")
    x2 = x2y2[:, :, 0]
    y2 = x2y2[:, :, 1]
    return ne.evaluate("sqrt(1 - (x2/a + y2/b))")


# x2+y2+z2 = 1
def sphere(xy, center=(0, 0), **kwargs):
    x2y2 = ne.evaluate("sum((xy-center)**2, axis=2)")
    return ne.evaluate("sqrt(1 - x2y2%1)")


def perspective_plane(xy, center=(0, 0), z=10, **kwargs):
    x2y2 = ne.evaluate("sum((xy-center)**2, axis=2)")
    z2 = z**2
    scale = 2 * math.pi
    return ne.evaluate("sqrt(x2y2+z2)*scale")


def fourier_plane(xy, center=(0, 0), **kwargs):
    x2y2 = ne.evaluate("sum((xy-center)**2, axis=2)")
    return x2y2


def exp_plane(xy, center=(0, 0), **kwargs):
    x2y2 = ne.evaluate("sum((xy-center)**2, axis=2)")
    return ne.evaluate("1/(x2y2)")


# z=x2-y2 h=c(x,y) * (x2-y2), c = x2+y2+z2
def hyperbolic_paraboloid(xy, center=(0, 0), **kwargs):
    x2y2 = ne.evaluate("(xy-center)**2")
    x2 = x2y2[:, :, 0]
    y2 = x2y2[:, :, 1]
    x2my2 = ne.evaluate("x2 - y2")
    return x2my2


# z=1/x2 - 1/y2
def reverse_paraboloid(xy, center=(0, 0), rotate=0, **kwargs):
    x2y2 = ne.evaluate("(xy-center)**2")
    x2 = x2y2[:, :, 0]
    y2 = x2y2[:, :, 1]
    x2my2 = ne.evaluate("1/x2 - 1/y2")
    return x2my2


# z=x3-3xy2
def monkey_saddle(xy, center=(0, 0), **kwargs):
    x = xy[:, :, 0] - center[0]
    y = xy[:, :, 1] - center[1]
    return ne.evaluate("x**3 - 3 * x * y**2")


def cartesian(r, angle):
    return np.stack([ne.evaluate("r*cos(angle)"), ne.evaluate("r*sin(angle)")], axis=2)


def polar(xy, z2=0):
    x2y2 = ne.evaluate("sum(xy**2, axis=2)")
    r = ne.evaluate("sqrt(x2y2 + z2)")
    x = xy[:, :, 0]
    y = xy[:, :, 1]
    angle = ne.evaluate("arctan2(y, x)")
    return r, angle


# pinch = math.pi
# 3 pinch = 4/3 * math.pi
# 2 pinch = 2*math.pi
def pinch_mod(xy, center=(0, 0), mod=4*math.pi/3, **kwargs):
    xy = xy - center
    # Convert to polar and do the above
    r, angle = polar(xy)
    # Mod angle, scale to [-pi/2 to pi/2],
    scale = math.pi/mod
    recenter = math.pi/2
    angle = ne.evaluate("angle % mod * scale - recenter")
    # Back to cartesian and then pinch
    return hyperbolic_paraboloid(cartesian(r, angle))


def contour(array, threshold=2*math.pi):
    return ne.evaluate("array % threshold")



def main():

    def get_default_params():
        return {
            "resolution": 300,
            "value_range": np.array([[-1, 1], [-1, 1]], dtype=np.float64),
            "threshold": 0.1,
            "center": [0, 0],
            "rotate": math.pi/12,
            "z": 10,
            "mod": math.pi,
            "hsv": True
        }

    def params_string(params):
        return f"p: {hl.tupliround(params['center'])}  " \
               f"z={params['z']}  " \
               f"mod={params['mod']}  " \
               f"range: {hl.tupliround(params['value_range'])} " \
               f"hsv={params['hsv']}  " \
               f"threshold={params['threshold']}  "

    params = get_default_params()
    xy_step = 1/8
    xy_scale = 1.1
    point_step = 0.1
    resolution_step = math.pi/64

    def image_func():
        funcs = [
            # sphere,
            # ellipsoid,
            # fourier_plane,
            perspective_plane,
            # reverse_paraboloid,
            # exp_plane,
            # hyperbolic_paraboloid,
            # monkey_saddle,
            # pinch_mod,
        ]

        xy = hl.xy_plane(value_range=params["value_range"], resolution=params["resolution"])
        planes = [f(xy=xy, center=(0, 0), mod=math.pi) for f in funcs]
        shifts = [f(xy=xy,
                    center=params["center"],
                    mod=params["mod"],
                    rotate=params["mod"])
                  for f in funcs]
        # diffs = [p + s for p, s in zip(planes, shifts)]

        planes = [contour(f, threshold=params["threshold"]) for f in planes]
        shifts = [-1*contour(f, threshold=-params["threshold"]) for f in shifts]
        diffs = [contour(p + s, threshold=params["threshold"]) for p, s in zip(planes, shifts)]
        contours = [
            hl.imagify(f, hsv=params["hsv"], bwref=[0, params["threshold"]])
            for f in [*planes, *shifts, *diffs]
        ]

        image = hl.tile_images(contours, num_cols=len(funcs))
        image = hl.add_text_bar(image, params_string(params))
        return image


    def key_func(key):
        length = params["value_range"][1][1] - params["value_range"][1][0]

        # WASD
        if key == ord("s"):  # Image coordinates are reversed! 0,0 is at the top left
            params["value_range"][1] += length*xy_step
        elif key == ord("w"):
            params["value_range"][1] -= length*xy_step
        elif key == ord("d"):
            params["value_range"][0] += length*xy_step
        elif key == ord("a"):
            params["value_range"][0] -= length*xy_step

        # ZX
        elif key == ord("z"):
            params["value_range"][:, 0] -= length*xy_step
            params["value_range"][:, 1] += length*xy_step
        elif key == ord("x"):
            params["value_range"][:, 0] += length*xy_step
            params["value_range"][:, 1] -= length*xy_step

        # PL;' (like wasd)
        elif key == ord("p"):
            params["center"][1] += point_step
        elif key == ord(";"):
            params["center"][1] -= point_step
        elif key == ord("l"):
            params["center"][0] += point_step
        elif key == ord("'"):
            params["center"][0] -= point_step

        elif key == ord("["):
            params["threshold"] -= point_step
        elif key == ord("]"):
            params["threshold"] += point_step

        # RE
        elif key == ord("r"):
            params["mod"] += resolution_step
        elif key == ord("e"):
            params["mod"] -= resolution_step if params["resolution"] > resolution_step else 0


        elif key == ord("h"):
            params["hsv"] = not params["hsv"]

        elif key == ord("."):
            params["value_range"] = get_default_params()["value_range"]

    hl.start_interactive(image_func, key_func)




if __name__ == "__main__":
    main()



################################################################################
# Tests
################################################################################

def test_polar():
    x = np.random.rand(100, 100)
    y = np.random.rand(100, 100)
    xy = np.stack([x, y], axis=2)
    r, angle = polar(xy)
    xyn = cartesian(r, angle)
    pprint(xy - xyn)
