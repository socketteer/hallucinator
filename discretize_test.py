import discretizer
import render
import math
import time
import obj

circle = obj.circle(20, [-5, -5])
set = discretizer.para_to_set(circle, [0, 2*math.pi], 100)

circle2 = obj.circle(10, [0, 0])
set2 = discretizer.para_to_set(circle2, [0, 2*math.pi], 100)

circle3 = obj.circle(5, [5, -10])
set3 = discretizer.para_to_set(circle3, [0, 2*math.pi], 100)

ray = obj.ray(math.pi / 4, [5, 5])
set4 = discretizer.para_to_set(ray, [0, 60], 100)

param, distance, vector = obj.vector([0, 30], [10, -20])
set5 = discretizer.para_to_set(vector, [0, param], distance)

img = render.set_to_bichrome(set.union(set2.union(set3.union(set4.union(set5)))),
                             -50, 50, -50, 50,
                             foreground=render.WHITE,
                             background=render.BLUE)
render.render_from_array(img)
