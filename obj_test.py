import obj
import scene

scene = scene.Scene()
scene.add_object(obj.vector((20, 10), (20, 100)))
scene.add_object(obj.rectangle(50, 100, (5, 50)))
scene.add_object(obj.circle(50, (100, 100)))
scene.add_object(obj.square(25, (150, 120)))
scene.add_object(obj.axes((-500, 500), (-500, 500), origin=(0, 0)))
scene.render(x_range=(-500, 500),
             y_range=(-500, 500))
