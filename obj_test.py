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
