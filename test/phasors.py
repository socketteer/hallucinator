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
hl.render_from_array(hl.imagify(zp1_phase, bwref=(0, 2*math.pi)))
hl.render_from_array(hl.imagify(zp2_phase, bwref=(0, 2*math.pi)))

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
