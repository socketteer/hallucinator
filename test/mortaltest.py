import hallucinator as hl
import math
import numpy as np
import numexpr as ne

points = hl.path_points((0, 5), density=10)
#print(points)

a_axis, b_axis = hl.surface_points(((0, 5), (0, 5)), density=(1, 1))
print(a_axis)
print(b_axis)


spiral = lambda p: (math.cos(p * 2 * math.pi),
                    p,
                    math.sin(p * 2 * math.pi))


def batch_spiral(p):
    tau = 2 * math.pi
    x = ne.evaluate("cos(p * tau)")
    y = p
    z = ne.evaluate("sin(p * tau)")
    return np.array([x, y, z])



surface_func = hl.plane_wave(0, 1)

spiral_sampled = hl.eval_path(spiral, points)
print(spiral_sampled)
spiral_sampled_2 = batch_spiral(points)
print('batch:')
print(spiral_sampled_2)

# plane_sampled = hl.eval_surf(surface_func, a_axis, b_axis)
# print(plane_sampled)
# print(plane_sampled.shape)
#
# ones = np.ones(plane_sampled.shape[1])
# arr = np.vstack((plane_sampled, ones))
# print(arr)
# rotated = np.matmul(hl.rotate_3(theta=math.pi/2), arr)
#
# print(rotated)