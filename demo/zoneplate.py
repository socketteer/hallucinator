import collections
import datetime
import sys
from functools import partial

import cv2

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import cmath

s = 0.5
power = 1.7


sizoneplate = lambda x, y: (x, y, sine_wave((x ** 2 + y ** 2) / s ** 2))
sqzoneplate = lambda x, y: (x, y, square_wave(pow(math.sqrt(x ** 2 + y ** 2), power) / s ** 2))

a_multiplier = 5
b_multiplier = 5


def sinezoneplate(params):
    point = sizoneplate(**params)
    return point


def squarezoneplate(params):
    point = sqzoneplate(**params)
    return point


def at_t(t):
    return sample(t * a_multiplier, t * b_multiplier)


def sample(a_density, b_density, at, params={}):
    print(params)
    points = hl.surface_region(at, params=params,
                               a_range=(-10, 10),
                               b_range=(-10, 10),
                               a_name='x',
                               b_name='y',
                               a_density=a_density,
                               b_density=b_density)
    canvas = hl.set_to_gradient(points=points,
                                x_range=(-10, 10),
                                y_range=(-10, 10),
                                black_ref=-1,
                                white_ref=1,
                                resolution=100,
                                default=hl.GRAY)
    print("canvas", type(canvas), canvas.shape, canvas)

    return canvas


################


################


# Waves
def sine_wave(x, **kwargs):
    return math.sin(x * math.tau)


def tan_wave(x, **kwargs):
    return max(-1.0, min(1.0, math.tan(x * math.tau)))


def square_wave(x, **kwargs):
    return -1 if x - math.floor(x) < 0.5 else 1


def twin_peaks_wave(x, **kwargs):
    x *= math.tau
    sin_x = math.sin(x)
    cos_x = math.cos(x)
    return pow(sin_x, 2)*cos_x


def sine_pow_wave(x, sine_power=3, **kwargs):
    return pow(sine_wave(x), sine_power)


# Plates
def spiral_plate(p, rotations=10, **kwargs):
    r, phi = cmath.polar(complex(p[0], p[1]))
    return math.sin(r ** 2 + (phi - math.pi / 2) * int(rotations))


def color_spiral_plate(p, rotations=5, **kwargs):
    v = spiral_plate(p, rotations=rotations)
    hsv_color = hl.np.uint8([[[(v + 1) * 127, 255, 255]]])
    color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)
    return color[0][0]


def hmm_plate(p, **kwargs):
    p2 = p ** 2
    return math.sin((p[0] + p[1]) * math.tau) * math.cos((p2[0] + p2[1]) * math.tau)


def perfectcolor(p, color_scale=1, **kwargs):
    radius2 = (p[0] ** 2 + p[1] ** 2)
    intensity = (sine_wave(radius2) + 1) * 127  # 0 to 255
    hue = int(radius2 * color_scale) % 255
    sat = hue
    hsv_color = hl.np.uint8([[[225 - hue, 255, 255]]])
    color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)
    return color[0][0]


def general_plate(p, periodic_function, radius_function, **kwargs):
    radius = hl.np.linalg.norm(p)
    return periodic_function(radius_function(radius, **kwargs), **kwargs)


def poly_plate(p, plate_power=2, periodic_function=sine_wave, **kwargs):
    return general_plate(p, periodic_function, (lambda r, **kw: math.pow(r, plate_power)), **kwargs)


def exp_plate(p, base=math.e, periodic_function=sine_wave, **kwargs):
    return general_plate(p, periodic_function, lambda r, **kw: math.pow(base, r), **kwargs)


def fib_plate(p, periodic_function=sine_wave, **kwargs):
    # https://en.wikipedia.org/wiki/Generalizations_of_Fibonacci_numbers#Extension_to_all_real_or_complex_numbers
    if not hasattr(fib_plate, "initialized"):
        fib_plate.sqrt5 = math.sqrt(5)
        fib_plate.phi = (1 + fib_plate.sqrt5) / 2
        fib_plate.initialized = True

    def continuous_fibonacci(x, **kwargs):
        phi_x = math.pow(fib_plate.phi, x)
        phi_neg_x = 1/phi_x
        return (phi_x - math.cos(x*math.pi)*phi_neg_x)/fib_plate.sqrt5

    return general_plate(p, periodic_function=periodic_function, radius_function=continuous_fibonacci, **kwargs)


def periodic_plate(p, periodic_function=sine_wave, radius_function=poly_plate, **kwargs):
    return general_plate(p,
                         periodic_function=periodic_function,
                         radius_function=lambda r, **kw: periodic_function(radius_function(r, **kwargs), **kwargs),
                         **kwargs)


# Given a dictionary which contains lists, find the longest length L
# Unroll all lists with len(L), creating a list of len(L) of dictionaries with the same
# key:value pairs, but a single value for each key which contained a list of len(L).
# Add a key __index to each dictionary corresponding to its place in the list
# This allows you to create param dicts which interpolate over multiple keys at the same time
def unroll_dict(dict_of_lists):
    # Find longest list in dict
    longest_len = 0
    for key, value in dict_of_lists.items():
        try:
            longest_len = max(longest_len, len(value))
        except Exception:
            pass

    # Make a list of dicts, unrolling the longest key lists
    list_of_dicts = []
    for i in range(longest_len):
        d = {}
        for key, value in dict_of_lists.items():
            try:
                if len(value) == longest_len:
                    d[key] = value[i]
                    continue
            except Exception:
                pass
            d[key] = value
        d["__index"] = i
        list_of_dicts.append(d)

    return list_of_dicts


if __name__ == "__main__":
    # file_prefix = "/home/bluis/Documents/hallucinator/videos/"
    file_prefix = "/Users/kylemcdonell/Code/Personal/hallucinator/demo/videos/zoneplates/"

    # hl.render_from_array(sample(20, 20, sinezoneplate))
    # hl.render_from_array(sample(20, 20, squarezoneplate))

    # hl.video(frame_func=lambda t: at_t(t),
    #          filename='zoneplates/fzp_moire_s{0}-da{1}-db{2}'.format(s, a_multiplier, b_multiplier),
    #          t_range=(0, 7),
    #          FPS=10)

    # hl.video(frame_func=lambda t: sample(20, 20, spiralzoneplate, {"scale": t, "rotations": 3}),
    #          filename='zoneplates/spiral_zp_scale_t={}-{}_fps={}'.format(0, 20, 2),
    #          t_range=(0, 1),
    #          FPS=5)

    # hl.interpolation_video(frame_function=perfectcolor,
    #                        t_param="scale",
    #                        t_range=(1, 500),
    #                        frames=400,
    #                        fps=5,
    #                        geometric_interp=True,
    #                        frame_size=(500, 500),
    #                        file_prefix='/home/bluis/Documents/hallucinator/videos/',
    #                        parallel=True)

    # hl.interpolation_video(frame_function=perfectcolor,
    #                        t_param="scale",
    #                        t_range=(10, 1000),
    #                        frames=1000,
    #                        fps=10,
    #                        geometric_interp=False,
    #                        frame_size=(1000, 1000),
    #                        file_prefix=file_prefix,
    #                        parallel=False)

    # params = {
    #         "value_function": partial(poly_plate, power=3),
    #         "x_range": (-10, 10),
    #         "y_range": (-10, 10),
    #     }
    # hl.render_from_array(hl.sampling_image(**params))

    # # Pow
    # hl.interpolation_video(value_function=exp_plate,
    #                        t_param="scale",
    #                        t_range=(1000, 10),
    #                        frames=100,
    #                        fps=5,
    #                        geometric_interp=False,
    #                        frame_size=(1000, 1000),
    #                        file_prefix='/Users/kylemcdonell/Code/Personal/hallucinator/demo/videos/zoneplates/',
    #                        parallel=False,
    #                        x_range=(-4, 4),
    #                        y_range=(-4, 4))

    # Exp
    # hl.interpolation_video(frame_function=poly_plate,
    #                        t_param="power",
    #                        t_range=(0.1, 5),
    #                        frames=100,
    #                        fps=5,
    #                        geometric_interp=False,
    #                        frame_size=(1000, 1000),
    #                        file_prefix='/Users/kylemcdonell/Code/Personal/hallucinator/demo/videos/zoneplates/',
    #                        parallel=False,
    #                        x_range=(-10, 10),
    #                        y_range=(-10, 10))



    # params = dict(
    #     frame_function=lambda d: hl.sampling_image(**d),
    #     frame_arguments=unroll_dict(dict(
    #         image_size=(500, 500),
    #         resolution=None,
    #         value_range=[(-100**(1/p), 100**(1/p)) for p in hl.np.geomspace(1, 1, num=100)],
    #         value_function=poly_plate,
    #         power=hl.np.geomspace(1, 5, num=100)
    #     )),
    #     filename=file_prefix + "temp-{}".format(datetime.datetime.now()),
    #     fps=5,
    #     preview=True,
    #     parallel=False,
    # )
    params = dict(
        frame_function=lambda d: hl.sampling_image(**d),
        frame_arguments=unroll_dict(dict(
            image_size=(500, 500),
            resolution=None, #hl.np.flip(hl.np.geomspace(10, 100, num=500)),
            value_range=hl.np.flip(hl.np.geomspace((-10, 10), (-1, 1), num=500)), #(-100, 100),
            value_function=periodic_plate,
            radius_function=exp_plate,
        )),
        filename=file_prefix + "temp-{}".format(datetime.datetime.now()),
        fps=10,
        preview=True,
        parallel=True,
    )
    hl.video2(**params)