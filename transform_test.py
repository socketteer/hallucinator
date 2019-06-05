import obj
import discretizer
import render

vector = obj.vector((20, 10), (20, 100))
v_set = discretizer.obj_to_set(vector)

rectangle = obj.rectangle(50, 100, (5, 50))
r_set = discretizer.obj_to_set(rectangle)

vector_rot = vector.rotate(200)
vr_set = discretizer.obj_to_set(vector_rot)

rect_rot = rectangle.rotate(45, (5, 50))
rr_set = discretizer.obj_to_set(rect_rot)

img = render.set_to_bichrome(v_set.union(r_set.union(vr_set.union(rr_set))),
                             (-200, 200), (-200, 200),
                             render.WHITE, render.BLUE)
render.render_from_array(img)
