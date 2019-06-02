import discretizer
import render
import math
import time
import objects

circle = objects.circle(20, [-5, -5])
set = discretizer.para_to_set(circle, 0, 2*math.pi, 100)
circle2 = objects.circle(10, [0, 0])
set2 = discretizer.para_to_set(circle2, 0, 2*math.pi, 100)
circle3 = objects.circle(5, [5, -10])
set3 = discretizer.para_to_set(circle3, 0, 2*math.pi, 100)
img = render.set_to_bichrome(set.union(set2.union(set3)), -50, 50, -50, 50, foreground=render.WHITE, background=render.BLUE)
render.render_from_array(img)
