import sys
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


def spiralwave(p, scale=5, rotations=200):
    r, phi = cmath.polar(complex(p[0], p[1]))
    return math.sin((r * scale) ** 2 + phi * int(rotations))


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


def create_image(value_function, params, x_range=(-1, 1), y_range=(-1, 1), image_width=500):
    print("Creating image with {}".format(params))
    x_axis = hl.np.linspace(start=x_range[0], stop=x_range[1], num=image_width)
    y_axis = hl.np.linspace(start=y_range[0], stop=y_range[1], num=image_width)

    # (x, y) for x in x_axis, y in y_axis
    meshgrid = hl.np.meshgrid(x_axis, y_axis)
    xy = hl.np.stack(meshgrid, axis=2)
    # Dimensions: (len(x_axis), len(y_axis), 2)

    # Apply the value function to each (x,y) in the grid. Might return a value or a [B,G,R]
    image_values = hl.np.apply_along_axis(lambda p: value_function(p, **params), 2, xy)

    # Normalised [0,255] as integer
    image = hl.np.interp(image_values, (image_values.min(), image_values.max()), (0, 255)).astype(hl.np.uint8)

    # If a single value was given, expand the array to dimensions: (len(x_axis), len(y_axis), 3)
    # if len(image.shape) == 2:
    #     image = hl.np.repeat(image[:, :, hl.np.newaxis], 3, axis=2)

    # hl.render_from_array(image)
    return image


function = spiralwave
function_name = spiralwave.__name__
t_param = "scale"
t_range = (0, 250)
frames = 900
fps = 5
frame_size = (500, 500)

# First and last frame
# hl.render_from_array(create_image(function, params={t_param: t_range[0]}, image_width=frame_size[0]))
# hl.render_from_array(create_image(function, params={t_param: t_range[1]}, image_width=frame_size[0]))

hl.parallel_video(frame_func=lambda t: create_image(function, params={t_param: t}, image_width=frame_size[0]),
                  t_range=t_range,
                  frames=frames,
                  fps=fps,
                  filename='zoneplates/{}_{}={}-{}_frames={}_fps={}'.format(function_name, t_param, *t_range, frames, fps))


# hl.render_from_array(sample(20, 20, sinezoneplate))
# hl.render_from_array(sample(20, 20, squarezoneplate))

# hl.video(frame_func=lambda t: at_t(t),
#          filename='zoneplates/fzp_moire_s{0}-da{1}-db{2}'.format(s, a_multiplier, b_multiplier),
#          t_range=(0, 7),
#          FPS=10)

# hl.parallel_video(frame_func=lambda t: sample(20, 20, spiralzoneplate, {"scale": t, "rotations": 3}),
#          filename='zoneplates/spiral_zp_scale_t={}-{}_fps={}'.format(0, 20, 2),
#          t_range=(0, 1),
#          FPS=5)