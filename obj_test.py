import objects
import discretizer
import render

vector = objects.vector([20, 10], [20, 100])
v_set = discretizer.obj_to_set(vector)


rectangle = objects.rectangle(50, 100, [5, 50])
r_set = discretizer.obj_to_set(rectangle)

img = render.set_to_bichrome(v_set.union(r_set), 0, 200, 0, 200, render.WHITE, render.BLUE)
render.render_from_array(img)
