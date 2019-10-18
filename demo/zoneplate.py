import sys
sys.path.append('../hallucinator')
import hallucinator as hl
import math
import cmath

s = 0.5
power = 1.7

squarewave = lambda t: -1 if t - math.floor(t) < 0.5 else 1
sinewave = lambda t: math.sin(t * 2 * math.pi)
sizoneplate = lambda x, y: (x, y, sinewave((x**2 + y**2) / s**2))
sqzoneplate = lambda x, y: (x, y, squarewave(pow(math.sqrt(x**2 + y**2), power) / s**2))

a_multiplier = 5
b_multiplier = 5


def spiralwave(x, y, scale=5, rotations=200):
    r, phi = cmath.polar(complex(x, y))
    return x, y, math.sin((r*scale)**2 + phi*rotations)


def spiral_zoneplate(params):
    point = spiralwave(**params)
    return point


def sinezoneplate(params):
    point = sizoneplate(**params)
    return point


def squarezoneplate(params):
    point = sqzoneplate(**params)
    return point


def at_t(t):
    return sample(t*a_multiplier, t*b_multiplier)


def sample(a_density, b_density, at):
    points = hl.surface_region(at, params={},
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

    return canvas


# hl.render_from_array(sample(20, 20, sinezoneplate))
# hl.render_from_array(sample(20, 20, squarezoneplate))
hl.render_from_array(sample(20, 20, spiral_zoneplate))

'''hl.video(frame_func=lambda t: at_t(t),
         filename='zoneplates/fzp_moire_s{0}-da{1}-db{2}'.format(s, a_multiplier, b_multiplier),
         t_range=(0, 7),
         FPS=10)'''