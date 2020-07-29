import collections
import datetime
import sys
import time
from functools import partial

import cv2
import hallucinator as hl
import math
import cmath

s = 0.5
power = 1.7


sizoneplate = lambda x, y: (x, y, sine_wave((x ** 2 + y ** 2) / s ** 2))
sqzoneplate = lambda x, y: (x, y, square_wave(pow(math.sqrt(x ** 2 + y ** 2), power) / s ** 2))



def fourier_zp(scale=1, center=(0, 0), phase=0):
    return lambda p: math.sin((((p[0]-center[0]) ** 2 + (p[1]-center[1]) ** 2) / s ** 2) / scale + phase)


def fourier_phase_zp(scale=1, center=(0, 0), phase=0):
    return lambda p: (((p[0]-center[0]) ** 2 + (p[1]-center[1]) ** 2) / s ** 2) / scale + phase


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
    # return math.sin((p[0] + p[1]) * math.tau) * math.cos((p2[0] + p2[1]) * math.tau)
    return math.sin((p[0] + p[1])) * math.cos((p2[0] + p2[1]))


def pinch_zone(p, **kwargs):
    return math.sin(p[0]**2 - p[1]**2)

def inverse_pinch(p, **kwargs):
    pinch = p[0]**2 - p[1]**2
    return math.sin(1/pinch if pinch!=0 else 0)

def square_zone(p, **kwargs):
    return math.sin(max(p[0]**2, p[1]**2))


def diamond_zone(p, **kwargs):
    return math.sin((abs(p[0])+abs(p[1]))**2)


def ellipse(p, **kwargs):
    return math.sin(0.25*p[0]**2 + p[1]**2)


def parabola(p, **kwargs):
    return math.sin(p[0]**2 + abs(p[1]))


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





if __name__ == "__main__":
    # file_prefix = "/home/bluis/Documents/hallucinator/videos/"
    file_prefix = "/Users/kylemcdonell/Code/Personal/hallucinator/demo/videos/"

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

    # params = dict(
    #     frame_function=lambda d: hl.sampling_image(**d),
    #     frame_arguments=hl.unroll_dict(dict(
    #         image_size=(500, 500),
    #         resolution=None,#hl.np.flip(hl.np.geomspace(4, 100, num=500)),
    #         value_range=hl.np.flip(hl.np.linspace((-0.001, 0.001), (-0.5, 0.5), num=3000)), #(-100, 100),
    #         # periodic_function=square_wave,
    #         # value_function=poly_plate,
    #         # plate_power=2,
    #         value_function=inverse_pinch,
    #         # value_function=periodic_plate,
    #         # radius_function=exp_plate,
    #     )),
    #     filename=file_prefix + "temp-{}".format(datetime.datetime.now()),
    #     fps=15,
    #     preview=True,
    #     parallel_frames=True,
    # )

    # def fresnel_plate(z=0, **kwargs):
    #     xy = hl.xy_plane(**kwargs)
    #     center = hl.np.array([0, 0])
    #     r2 = hl.ne.evaluate("sum((xy-center)**2, axis=2)")
    #     wave = hl.ne.evaluate("sin(sqrt(r2+z**2))")
    #     # print(f"Created frame for {t}")
    #
    #     return wave
    #     # hl.np.mod(phase, 2*math.pi)/2*math.pi
    #     # return 0 if phase % 2*math.pi > math.pi else 255
    #
    # params = dict(
    #     frame_function=lambda d: hl.imagify(fresnel_plate(**d), bwref=[-1, 1]),
    #     frame_arguments=hl.unroll_dict(dict(
    #         resolution=(500, 500),
    #         value_range=hl.np.flip(hl.np.linspace((-50000, 50000), (-50, 50), num=10000)), #(-100, 100),
    #     )),
    #     filename=file_prefix + "temp-{}".format(datetime.datetime.now()),
    #     fps=60,
    #     preview=True,
    #     parallel_frames=False,
    # )
    # hl.video(**params)


    def fresnel_pinch(z=100, **kwargs):
        center = 0j
        xy = hl.complex_plane(**kwargs)
        x = xy.real
        y = xy.imag

        x2 = hl.ne.evaluate("(x-center.real)**2")
        y2 = hl.ne.evaluate("(y-center.imag)**2")


        # sined = hl.ne.evaluate("sin(x2-y2)")
        return hl.ne.evaluate("sin(sqrt(x2-y2+z)**2)")
        # hl.render_from_array(hl.imagify(sined, bwref=[-1, 1]))
        # exit()


    params = dict(
        frame_function=lambda d: hl.imagify(fresnel_pinch(**d), bwref=[-1, 1]),
        frame_arguments=hl.unroll_dict(dict(
            resolution=(500, 500),
            value_range=hl.np.flip(hl.np.linspace((-1000, 1000), (1, -1), num=5000)), #(-100, 100),
        )),
        filename=file_prefix + "temp-{}".format(datetime.datetime.now()),
        fps=60,
        preview=True,
        parallel_frames=False,
    )
    # hl.video(**params)

    def three_pinch(wrap=3/2, **kwargs):
        c = hl.complex_plane(**kwargs)
        p_2 = math.pi/2
        # (x.real / (-x.real): -1 if x>0, 1 if x<0
        # +Pi if x<0
        theta = hl.ne.evaluate("arctan2(c.imag, c.real) + p_2 + p_2 * (c.real / (-c.real))")
        pinch = hl.ne.evaluate("sin((c.real**2+c.imag**2) * abs(sin(wrap * theta)))")
        return pinch

    # print(params["frame_arguments"][0])
    # hl.render_from_array(hl.imagify(three_pinch(**params["frame_arguments"][0]), bwref=[-1, 1])),
    params = dict(
        frame_function=lambda kwargs: hl.imagify(three_pinch(**kwargs, bwref=[-1, 1])),
        frame_arguments=hl.unroll_dict(dict(
            resolution=(500, 500),
            value_range=hl.np.flip(hl.np.geomspace((-10000, 10000), (-10, 10), num=1000))), #(-100, 100),
        ),
        filename=file_prefix + "temp-{}".format(datetime.datetime.now()),
        fps=30,
        preview=True,
        parallel_frames=False,
    )
    hl.video(**params)


    # phasors!!

    # def phasor(p, t, **kwargs):
    #     r = sum(p**2)
    #     phase = t*r*2*math.pi/100
    #     return 0 if phase % 2*math.pi > math.pi else 255
    #
    # def phase_image(t, **kwargs):
    #     # Freq increase
    #     xy = hl.xy_plane(**kwargs)
    #     center = hl.np.array([0, 0])
    #     r2 = hl.ne.evaluate("sum((xy-center)**2, axis=2)")
    #     zp1 = hl.ne.evaluate("sin(t*r2)")
    #     zp1 = hl.add_text_bar(hl.imagify(zp1, bwref=[-1, 1]), "freq increase")
    #
    #     # Range increase
    #     value_range = kwargs.pop("value_range")
    #     value_range[0] -= t
    #     value_range[1] += t
    #     xy = hl.xy_plane(value_range, **kwargs)
    #     center = hl.np.array([0, 0])
    #     r2 = hl.ne.evaluate("sum((xy-center)**2, axis=2)")
    #     zp2 = hl.ne.evaluate("sin(r2)")
    #     zp2 = hl.add_text_bar(hl.imagify(zp2, bwref=[-1, 1]), "range increase")
    #
    #     print(f"Created frame for {t}")
    #     img = hl.tile_images([zp1, zp2])
    #     return img
    #
    #
    # params = dict(
    #     frame_function=lambda d: phase_image(**d),
    #     frame_arguments=hl.unroll_dict(dict(
    #         resolution=(1000, 1000),
    #         # resolution=hl.np.flip(hl.np.geomspace(4, 100, num=500)),
    #         t=hl.np.linspace(0, 10*math.pi, num=100),
    #         value_range=hl.np.array([-1., 1.]),
    #     )),
    #     filename=f"{file_prefix}temp-{format(datetime.datetime.now())}",
    #     fps=15,
    #     preview=True,
    #     parallel_frames=False,
    # )
    # hl.video(**params)
