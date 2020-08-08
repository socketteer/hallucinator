import math
import sys
import numpy as np
sys.path.append('../hallucinator')

import hallucinator as hl

def birth(t, **kwargs):
    val_range = 200
    plane = np.zeros((val_range, val_range))  # hl.xy_plane(value_range=(0, val_range), resolution=val_range)
    size = 30
    # center = (val_range/2, val_range/2)
    split = val_range / 2
    init_offset = val_range / 4
    offset_scale = 100

    for x in range(val_range):
        for y in range(val_range):
            if x > split:
                if y > split:
                    """ lower right """
                    plane[x][y] = math.sin(((x - split - offset_scale*math.cos(t)) ** 2
                                            + (y - split - offset_scale*math.sin(t)) ** 2
                                            + (offset_scale*math.cos(t))**2 + (offset_scale*math.sin(t))**2)
                                           / size + math.pi/2)
                else:
                    """lower left"""
                    plane[x][y] = 0
                    plane[x][y] = math.sin(((x - split - offset_scale*math.cos(t)) ** 2
                                            - (y - split + offset_scale*math.sin(t)) ** 2
                                            - (offset_scale * math.cos(t)) ** 2 + (offset_scale*math.sin(t))**2)
                                           / size + math.pi/2)
            else:
                if y > split:
                    """ upper right """
                    plane[x][y] = math.sin(((x - split + offset_scale*math.cos(t)) ** 2
                                            - (y - split - offset_scale*math.sin(t)) ** 2
                                           - (offset_scale * math.cos(t))**2 - (offset_scale*math.cos(t))**2)
                                           / size)# - math.pi / 2)
                else:
                    """ upper left """
                    plane[x][y] = math.sin(((x - split + offset_scale*math.cos(t)) ** 2
                                            + (y - split + offset_scale*math.sin(t)) ** 2
                                            + (-offset_scale * math.cos(t))**2 + (offset_scale*math.sin(t))**2)
                                           / size)
    return hl.imagify(plane, hsv=False)


#hl.render_from_array(hl.imagify(birth(1000)))
'''filename = '../images/zonepinch{0}.png'.format(offset)
hl.save_img(img, filename)'''

params = dict(
        frame_function=lambda d: birth(**d),
        frame_arguments=hl.unroll_dict(dict(
            t=hl.np.linspace(0, math.pi, num=200),
        )),
        filename=f"../videos/birth",
        fps=10,
        preview=True,
        parallel_frames=False,
    )

hl.video(**params)

