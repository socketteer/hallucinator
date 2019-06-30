import obj3
import scene


scene = scene.Scene3()
box = obj3.box(200, 200, 200, (0, 0, 500))
scene.add_object(box)
scene.add_object(box.rotate(30, axis='Y'))
scene.add_object(box.rotate(90, axis='Y'))
scene.add_object(box.rotate(150, axis='Y'))


scene.add_object(obj3.axes((-5000, 5000), (-5000, 5000), (-5000, 5000), origin=(200, 300, 500)))
scene.lazy_render(x_range=(-1000, 1000),
                  y_range=(-1000, 1000))
