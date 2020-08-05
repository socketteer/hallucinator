import hallucinator as hl

points = hl.path_points((0, 5), density=10)
print(points)

points2 = hl.surface_points(((0, 5), (0, 5)), density=(1, 1))
print(points2)
