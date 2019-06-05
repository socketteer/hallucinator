import obj3
import discretizer
import render

points_set = set()

for i in range(-3, 3):
    for j in range(-3, 3):
        for k in range(-3, 3):
            new_box = obj3.box(200, 200, 200, (i*250, j*250, 500 + k*250))
            box_set = discretizer.obj_to_set(new_box)
            box_proj_set = render.project(box_set)
            points_set = points_set.union(box_proj_set)

arr = render.set_to_bichrome(points_set,
                             x_range=(-1000, 1000),
                             y_range=(-1000, 1000))
render.render_from_array(arr)
render.save_img(arr, 'hyperzoom.jpg')
