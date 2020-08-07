import hallucinator as hl
import math
import numpy as np
import numexpr as ne

points = hl.surface_points(surface_range=((0, 4), (0, 4)))
#print(points.shape)

func = hl.gen_plane_wave()
sampled = func(points)
h1 = sampled[:, :, 1:]
h2 = sampled[:, :, :-1]
v1 = sampled[:, 1:, :]
v2 = sampled[:, :-1, :]
h1_reshaped = hl.reshape_array(h1)
h2_reshaped = hl.reshape_array(h2)
v1_reshaped = hl.reshape_array(v1)
v2_reshaped = hl.reshape_array(v2)

h1_transformed = np.matmul(hl.rotate_3(theta=math.pi/4, axis=(0, 0, 1)), h1_reshaped)
h2_transformed = np.matmul(hl.rotate_3(theta=math.pi/4, axis=(0, 0, 1)), h2_reshaped)
v1_transformed = np.matmul(hl.rotate_3(theta=math.pi/4, axis=(0, 0, 1)), v1_reshaped)
v2_transformed = np.matmul(hl.rotate_3(theta=math.pi/4, axis=(0, 0, 1)), v2_reshaped)

h = np.array((h1_transformed, h2_transformed))
h_transpose = h.transpose()
h_swapped = np.swapaxes(h_transpose, 1, 2)
v = np.array((v1_transformed, v2_transformed))
v_transpose = v.transpose()
v_swapped = np.swapaxes(v_transpose, 1, 2)

lines = np.concatenate((h_swapped, v_swapped), axis=0)

im = hl.lines_to_bichrome(lines, (-10, 10), (-10, 10), resolution=50)
hl.render_from_array(im)

# print(sampled)
# im = hl.points_to_bichrome(sampled.transpose(), (-10, 10), (-10, 10), resolution=50)
# hl.render_from_array(im)