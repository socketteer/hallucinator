import hallucinator as hl
import math


def phasor_product(f1, f2):
    return lambda p: (f1(p) - f2(p)) % (2 * math.pi)


zp = hl.fourier_phase_zp(10)
zp2 = hl.fourier_phase_zp(10, phase=0.3)
zp3 = hl.fourier_phase_zp(10, phase=math.pi)
zp4 = hl.fourier_phase_zp(10, phase=4)



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
hl.render_from_array(plane)

# 0 1 2 0 1 2 0 1 2
# 2 0 1 2 0 1 2 0 1
# 2 1 0 2 1 0 2 1 0
# 1 1 1 1 1 1 1 1 1

# (a + b) mod n == (a - (n-b)) mod n
