import objects
import discretizer
import render

vector = objects.vector((20, 10), (20, 100))
v_set = discretizer.obj_to_set(vector)


rectangle = objects.rectangle(50, 100, (5, 50))
r_set = discretizer.obj_to_set(rectangle)

circle = objects.circle(50, (100, 100))
c_set = discretizer.obj_to_set(circle)

square = objects.square(25, (150, 120))
s_set = discretizer.obj_to_set(square)

img = render.set_to_bichrome(v_set.union(r_set.union(c_set.union(s_set))),
                             (0, 200), (0, 200),
                             render.WHITE, render.BLUE)
render.render_from_array(img)


sin = objects.wave(50, 0.01, 20)
sin_set = discretizer.para_to_set(sin, (-1000, 1000), 10000)
sin_img = render.set_to_bichrome(sin_set, (-1000, 1000), (-100, 100))
render.render_from_array(sin_img)
