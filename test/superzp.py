import hallucinator as hl
import math

zp = hl.fourier_zp(10)
zp_pi = hl.fourier_zp(10, phase=math.pi)
zp1 = hl.fourier_zp(15, (-0.5, 0))
zp1_pi = hl.fourier_zp(15, (-0.5, 0), math.pi)
zp2 = hl.fourier_zp(15, (0.5, 0))
zp2_pi = hl.fourier_zp(15, (0.5, 0), math.pi)

plane = hl.sampling_image(lambda p: abs(zp1(p) + zp2(p)), value_range=(-10, 10), image_size=(1000, 1000), binary=False)
hl.render_from_array(plane)

'''plane = hl.sampling_image(zp, value_range=(-10, 10), image_size=(800, 800), binary=False)
hl.render_from_array(plane)

plane = hl.sampling_image(zp_pi, value_range=(-10, 10), image_size=(800, 800), binary=False)
hl.render_from_array(plane)'''