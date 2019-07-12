import sys
sys.path.append('../ikonal')
import ikonal

plane = ikonal.plane((0, 0, 0), (0, 0, 1), (1, 1, 0))

print(plane(0, 0))
print(plane(1, 0))
print(plane(0, 1))
print(plane(1, 1))

print(plane(1, -1))

frame = ikonal.Scene3()
frame.add_object(ikonal.axes_3((-5000, 5000), (-5000, 5000), (-5000, 5000), origin=(0, 0, 0)))
