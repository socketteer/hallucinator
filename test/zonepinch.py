import math
import sys
import numpy as np
sys.path.append('../hallucinator')

import hallucinator as hl

'''val_range = 2000
plane = np.zeros((val_range, val_range))#hl.xy_plane(value_range=(0, val_range), resolution=val_range)
size = 1000
#center = (val_range/2, val_range/2)
split = val_range/2
num_images = 3
offsets = [1000, 2000, 3000]
for i in range(num_images):
    for x in range(val_range):
        for y in range(val_range):
            if x > split:
                plane[x][y] = math.sin(((x - split + offsets[i]) ** 2
                                        + (y-val_range/2)**2 - 2*(offsets[i])**2)
                                       / size)
            else:
                plane[x][y] = math.sin(((x - split - offsets[i]) ** 2
                                        - (y-val_range/2) ** 2)
                                       / size + math.pi)

    img = hl.imagify(plane, hsv=False)
    hl.render_from_array(img)'''


def birth(t, **kwargs):
    val_range = 1000
    plane = np.zeros((val_range, val_range))  # hl.xy_plane(value_range=(0, val_range), resolution=val_range)
    size = 500
    # center = (val_range/2, val_range/2)
    split = val_range / 2
    offset_scale = 1
    offset = offset_scale*t
    for x in range(val_range):
        for y in range(val_range):
            if x > split:
                plane[x][y] = math.sin(((x - split + offset) ** 2
                                        + (y - val_range / 2) ** 2 - 2 * offset ** 2)
                                       / size)
            else:
                plane[x][y] = math.sin(((x - split - offset) ** 2
                                        - (y - val_range / 2) ** 2)
                                       / size + math.pi)
    return hl.imagify(plane)


'''filename = '../images/zonepinch{0}.png'.format(offset)
hl.save_img(img, filename)'''

params = dict(
        frame_function=lambda d: birth(**d),
        frame_arguments=hl.unroll_dict(dict(
            t=hl.np.linspace(2000, -2000, num=1000),
        )),
        filename=f"birth4",
        fps=30,
        preview=True,
        parallel_frames=False,
    )

hl.video(**params)

