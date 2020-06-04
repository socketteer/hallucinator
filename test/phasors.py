import hallucinator as hl
import math


def phasor_delay(f1, f2):
    return lambda p: (f1(p) - f2(p)) % (2 * math.pi)


'''zp = hl.fourier_phase_zp(10)
zp2 = hl.fourier_phase_zp(10, phase=0.3)
zp3 = hl.fourier_phase_zp(10, phase=math.pi)
zp4 = hl.fourier_phase_zp(10, phase=4)'''

xy = hl.xy_plane(value_range=(-10, 10))
persp_xy = hl.perspective_plane(xy, p=(0, 0, 100))
persp_xy_2 = hl.perspective_plane(xy, p=(0, 0, 100))
zp_opl = hl.opl_zp(persp_xy)
zp_opl_2 = hl.phase_conjugate(hl.opl_zp(persp_xy_2))
#zp_opl_2 = hl.opl_zp(persp_xy)
zp1_phase = hl.phase_threshold(zp_opl)
zp2_phase = hl.phase_threshold(zp_opl_2)
zp1_r = hl.real(zp1_phase)
zp2_r = hl.real(zp2_phase)
zp1_i = hl.imaginary(hl.phase_threshold(zp_opl))
zp2_i = hl.imaginary(hl.phase_threshold(zp_opl_2))
''''hl.render_from_array(hl.imagify(zp1, bwref=(-1, 1)))
hl.render_from_array(hl.imagify(zp2, bwref=(-1, 1)))
hl.render_from_array(hl.imagify(zp1_i, bwref=(-1, 1)))
hl.render_from_array(hl.imagify(zp2_i, bwref=(-1, 1)))'''
#hl.render_from_array(hl.imagify(zp1_phase, bwref=(0, 2*math.pi)))
#hl.render_from_array(hl.imagify(zp2_phase, bwref=(0, 2*math.pi)))

'''hl.plot_images([hl.imagify(zp1_phase, bwref=(0, 2*math.pi)), hl.imagify(zp2_phase, bwref=(0, 2*math.pi))],
               titles=['original', 'conjugate'])'''


def zoneplate_product():
    xy = hl.xy_plane(value_range=(-10, 10), resolution=500)
    example_params = dict(
        image_funcs=[
            lambda a, b: hl.phase_threshold(hl.opl_zp(hl.perspective_plane(xy, p=[0, 0, a]))),
            lambda a, b: hl.phase_conjugate(hl.phase_threshold(hl.opl_zp(hl.perspective_plane(xy, p=[0, 0, b])))),
            lambda a, b: hl.phase_threshold(hl.opl_zp(hl.perspective_plane(xy, p=[0, 0, a])
                         + hl.phase_conjugate(hl.opl_zp(hl.perspective_plane(xy, p=[0, 0, b])))))
        ],
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
        image_funcs=[
            lambda z, zoom: hl.perspective_zp(hl.perspective_plane(hl.xy_plane(value_range=(-zoom, zoom), resolution=500),
                                                                p=[0, 0, z]))
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
            p=[x, y, z], xy=hl.xy_plane(value_range=(-zoom, zoom), resolution=200)))

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

#zoneplate_product()
#zoneplate()
focus()

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
