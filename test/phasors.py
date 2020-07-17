from enum import Enum
from functools import lru_cache

import hallucinator as hl
import math

def phasor_delay(f1, f2):
    return lambda p: (f1(p) - f2(p)) % (2 * math.pi)


'''zp = hl.fourier_phase_zp(10)
zp2 = hl.fourier_phase_zp(10, phase=0.3)
zp3 = hl.fourier_phase_zp(10, phase=math.pi)
zp4 = hl.fourier_phase_zp(10, phase=4)'''

# xy = hl.xy_plane(value_range=(-10, 10))
# persp_xy = hl.perspective_plane(xy, p=(0, 0, 100))
# persp_xy_2 = hl.perspective_plane(xy, p=(0, 0, 100))
# zp_opl = hl.opl_zp(persp_xy)
# zp_opl_2 = hl.phase_conjugate(hl.opl_zp(persp_xy_2))
# #zp_opl_2 = hl.opl_zp(persp_xy)
# zp1_phase = hl.phase_threshold(zp_opl)
# zp2_phase = hl.phase_threshold(zp_opl_2)
# zp1_r = hl.real(zp1_phase)
# zp2_r = hl.real(zp2_phase)
# zp1_i = hl.imaginary(hl.phase_threshold(zp_opl))
# zp2_i = hl.imaginary(hl.phase_threshold(zp_opl_2))
''''hl.render_from_array(hl.imagify(zp1, bwref=(-1, 1)))
hl.render_from_array(hl.imagify(zp2, bwref=(-1, 1)))
hl.render_from_array(hl.imagify(zp1_i, bwref=(-1, 1)))
hl.render_from_array(hl.imagify(zp2_i, bwref=(-1, 1)))'''
#hl.render_from_array(hl.imagify(zp1_phase, bwref=(0, 2*math.pi)))
#hl.render_from_array(hl.imagify(zp2_phase, bwref=(0, 2*math.pi)))

'''hl.plot_images([hl.imagify(zp1_phase, bwref=(0, 2*math.pi)), hl.imagify(zp2_phase, bwref=(0, 2*math.pi))],
               titles=['original', 'conjugate'])'''


def zoneplate_product():
    xy = hl.xy_plane(value_range=(-10, 10), resolution=300)

    def images_func(a, b):
        zp1 = hl.opl_zp(hl.perspective_plane(xy, p=[0, 0, a]))
        zp2 = hl.phase_conjugate(hl.opl_zp(hl.perspective_plane(xy, p=[0, 0, b])))
        zp3 = zp1 + zp2

        return [hl.phase_threshold(zp) for zp in [zp1, zp2, zp3]]
    example_params = dict(
        images_func=lambda a, b: images_func(a, b),
        num_image=3,
        titles=[
            "zp1",
            "zp2",
            "product"
        ],
        slider_params=[
            ["a", 0, 100],
            ["b", 0, 100],
        ]
    )
    hl.create_interactive_plot(**example_params)



def zoneplate():
    params = dict(
        images_func=[
            lambda z, zoom: [hl.perspective_zp(hl.perspective_plane(
                hl.xy_plane(value_range=(-zoom, zoom), resolution=500),
                p=[0, 0, z]))]
        ],
        titles=[
            "perspective zone plate"
        ],
        slider_params=[
            ["z", 0, 5],
            ["zoom", 0.01, 20],
        ]
    )
    hl.create_interactive_plot(**params)


def focus():
    def zp_func(x, y, z, zoom):
        return hl.opl_zp(hl.perspective_plane(
            p=[x, y, z], xy=hl.xy_plane(value_range=(-zoom, zoom), resolution=1000)))

    def images_func(a, b):
        pass
    # source = lambda x, y, z, zoom: hl.imagify(hl.phase_threshold(zp_func(0, 0, 10, zoom)),
    #                                           bwref=(0, 2*math.pi))
    # perspective = lambda x, y, z, zoom: hl.imagify(hl.phase_threshold(hl.phase_conjugate(zp_func(x, y, z, zoom))),
    #                                                bwref=(0, 2*math.pi))
    product = lambda x, y, z, zoom: hl.imagify(hl.phase_threshold(zp_func(0, 0, 10, zoom)
                                                                  + hl.phase_conjugate(zp_func(x, y, z, zoom))),
                                               bwref=(0, 2*math.pi))

    params = dict(
        image_funcs=[
            # source,
            # perspective,
            product
        ],
        titles=[
            # "source", "perspective",
            "product"
        ],
        slider_params=[
            ["x", -10, 10],
            ["y", -10, 10],
            ["z", 0, 20],
            ["zoom", 0.01, 20],
        ]
    )
    hl.create_interactive_plot(**params)


def weird_space():
    def zp_func(x, y, z, zoom):
        return hl.opl_zp(hl.perspective_plane(
            p=[x, y, z], xy=hl.xy_plane(value_range=(-zoom, zoom), resolution=500)))

    @lru_cache(maxsize=30)
    def zp1_func(zoom):
        return hl.phase_conjugate(zp_func(0,0,10,zoom))


    def images_func(t, z, zoom):
        zp1 = zp1_func(zoom)
        zp2 = zp_func(t*math.cos(t), t*math.sin(t), z, zoom)
        zp3 = zp1 + zp2
        return [hl.phase_threshold(zp) for zp in [zp1, zp2, zp3]]

    params = dict(
        images_func=lambda t, z, zoom: images_func(t, z, zoom),
        num_images=3,
        titles=[
            "zp1=conj(0, 0, 10, zoom)",
            "zp2=(tcost, tsint, z, zoom)",
            "zp3=zp1+zp2"
        ],
        slider_params=[
            ["t", -10, 10],
            ["z", 0, 5],
            ["zoom", 0.01, 20],
        ]
    )
    hl.create_interactive_plot(**params)

# weird_space()


#zoneplate_product()
#zoneplate()
# focus()

def vid():
    def zp_func(x, y, z, zoom):
        return hl.opl_zp(hl.perspective_plane(
            p=[x, y, z], xy=hl.xy_plane(value_range=(-zoom, zoom), resolution=500)))

    def zp(zoom):
        return hl.phase_conjugate(zp_func(0, 0, 10, zoom))
    zp10 = zp(1)
    zp10pt = hl.phase_threshold(zp10)

    def percieve_zp(zp1, zp2):
        # zp2pt = hl.phase_threshold(zp2)
        zp1 = hl.phase_threshold(zp1)
        zp2 = hl.phase_threshold(zp2)
        zp3 = hl.phase_threshold(zp1 + zp2)
        # print(zp2)
        # combined1 = hl.np.concatenate([zp3, zp10pt])
        # combined2 = hl.np.concatenate([zp2pt, zp3])
        # combined = hl.np.hstack([combined1, combined2])
        # return hl.imagify(zp3, hsv=True, bwref=(0, 2*math.pi))

        return hl.imagify(zp3, hsv=False, bwref=(0, 2*math.pi))

    def filenamer(x=0, y=0, z=10, zoom=10, range=(-10, 10)):
        return f"crazy_thing.png_x={x}_y={y}_z={z}_zoom={zoom}_range={str(range)}_res={500}"


    hl.render_from_array(hl.imagify(
        percieve_zp(zp10, zp_func(1, 1, 10, 1)),
        hsv=False, bwref=(0, 2*math.pi))
    )

    return

    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp10, zp_func(10, 10, 10*math.sin(t)+10, 10)),
    #     frame_arguments=hl.np.linspace(0, 10, num=3000),
    #     fps=30,
    #     filename=filenamer(z="10sin(t)+10", range=(0, 10)),
    #     parallel_frames=True
    # )
    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp10, zp_func(0, 0, t, 10)),
    #     frame_arguments=hl.np.linspace(0, 30, num=3000),
    #     fps=30,
    #     filename=filenamer(z="t", range=(0, 30)),
    #     parallel_frames=True
    # )
    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp10, zp_func(t, 0, 10, 10)),
    #     frame_arguments=hl.np.linspace(-20, 20, num=3000),
    #     fps=30,
    #     filename=filenamer(x="t", range=(-20, 20)),
    #     parallel_frames=True
    # )
    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp(t), zp_func(0, 0, 5, t)),
    #     frame_arguments=hl.np.linspace(0, 400, num=3000)[::-1],
    #     fps=10,
    #     filename=filenamer(z=5, zoom="t", range=(400, 0)),
    #     parallel_frames=True
    # )
    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp10, zp_func(t, 0, t+10, 10)),
    #     frame_arguments=hl.np.linspace(-20, 20, num=3000),
    #     fps=30,
    #     filename=filenamer(x="t", z="t+10", range=(-20, 20)),
    #     parallel_frames=True
    # )
    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp10, zp_func(t, 0, 5*math.sin(t)+5, 10)),
    #     frame_arguments=hl.np.linspace(-6, 6, num=3000),
    #     fps=30,
    #     filename=filenamer(x="t", z="5sin(t)+5", range=(-6, 6)),
    #     parallel_frames=True
    # )
    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp10, zp_func(t*math.cos(t), 0, 10+t*math.sin(t), 10)),
    #     frame_arguments=hl.np.linspace(-10, 10, num=3000),
    #     fps=30,
    #     filename=filenamer(x="tcos(t)", z="10+tsin(t)", range=(-10, 10)),
    #     parallel_frames=True
    # )
    hl.video(
        frame_function=lambda t: percieve_zp(zp10, zp_func(100*math.cos(t), 100*math.sin(t), 15, 10)),
        frame_arguments=hl.np.linspace(0, math.pi, num=600),
        fps=60,
        filename=filenamer(x="cos(t)", y="sin(t)", range=(0, 2*math.pi)),
        parallel_frames=True,
        preview=True
    )
    #
    # def cube_path(t):
    #     if t<10:
    #         return dict(z=10+t, x=0, y=0)
    #     t -= 10
    #     if t<10:
    #         return dict(z=10+10, x=t, y=0)
    #     t -= 10
    #     if t<10:
    #         return dict(z=10+10, x=10, y=t)
    #     t -= 10
    #     if t<10:
    #         return dict(z=10+10-t, x=10, y=10)
    #     t -= 10
    #     if t<10:
    #         return dict(z=10, x=10-t, y=10)
    #     t -= 10
    #     return dict(z=10, x=0, y=10-t)
    #
    # hl.video(
    #     frame_function=lambda t: percieve_zp(zp10, zp_func(**cube_path(t), zoom=10)),
    #     frame_arguments=hl.np.linspace(0, 60, num=2000),
    #     fps=30,
    #     filename="crazy_thing.png_cube_path-z-x-y-(10,10,10)",
    #     parallel_frames=True
    # )

vid()




'''zp_delay_opl = zp_opl + zp_opl_2
zp_delay = hl.real(hl.phase_threshold(zp_delay_opl))
hl.render_from_array(hl.imagify(zp_delay, bwref=(-1, 1)))'''



'''
plane = hl.sampling_image(lambda p: math.sin(phasor_product(zp, zp)(p)), value_range=(0, 10), bw_points=(-1, 1),
                          image_size=(800, 800), binary=False)
hl.render_from_array(plane)

plane = hl.sampling_image(lambda p: math.sin(phasor_product(zp, zp2)(p)), value_range=(0, 10), image_size=(800, 800),
                          bw_points=(-1, 1), binary=False)
hl.render_from_array(plane)

plane = hl.sampling_image(lambda p: math.sin(phasor_product(zp, zp3)(p)), value_range=(0, 10), image_size=(800, 800),
                          bw_points=(-1, 1), binary=False)
hl.render_from_array(plane)

plane = hl.sampling_image(lambda p: math.sin(phasor_product(zp, zp4)(p)), value_range=(0, 10), image_size=(800, 800),
                          bw_points=(-1, 1), binary=False)
hl.render_from_array(plane)'''

# 0 1 2 0 1 2 0 1 2
# 2 0 1 2 0 1 2 0 1
# 2 1 0 2 1 0 2 1 0
# 1 1 1 1 1 1 1 1 1

# (a + b) mod n == (a - (n-b)) mod n
