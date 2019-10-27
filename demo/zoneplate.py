import collections
import sys

import cv2

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import cmath

s = 0.5
power = 1.7

squarewave = lambda t: -1 if t - math.floor(t) < 0.5 else 1
sinewave = lambda t: math.sin(t * 2 * math.pi)
sizoneplate = lambda x, y: (x, y, sinewave((x ** 2 + y ** 2) / s ** 2))
sqzoneplate = lambda x, y: (x, y, squarewave(pow(math.sqrt(x ** 2 + y ** 2), power) / s ** 2))

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


def spiralwave(p, scale=20, rotations=10, **kwargs):
    r, phi = cmath.polar(complex(p[0] * scale, p[1] * scale))
    return math.sin(r ** 2 + (phi - math.pi / 2) * int(rotations))


def colorspiral(p, scale=5, rotations=5, **kwargs):
    r, phi = cmath.polar(complex(p[0] * scale, p[1] * scale))
    v = math.sin(r ** 2 + (phi - math.pi / 2) * int(rotations))

    hsv_color = hl.np.uint8([[[(v+1)*127, 255, 255]]])
    color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)
    return color[0][0]


def hmm(p, scale=10, **kwargs):
    p = p * scale
    p2 = p ** 2
    return math.sin((p[0] + p[1]) * 2 * math.pi) * math.cos((p2[0] + p2[1]) * 2 * math.pi)


def perfectplate(p, scale=100, **kwargs):
    return sinewave(scale * (p[0] ** 2 + p[1] ** 2))



if __name__ == "__main__":
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

    hl.interpolation_video(frame_function=colorspiral,
                           t_param="resolution",
                           t_range=(500, 100),
                           frames=100,
                           fps=5,
                           frame_size=(500, 500))
