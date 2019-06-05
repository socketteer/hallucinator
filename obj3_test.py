import obj3
import scene


scene = scene.Scene3()
scene.add_object(obj3.box(200, 200, 200, (250, 250, 500)))
scene.add_object(obj3.axes((-5000, 5000), (-5000, 5000), (-5000, 5000), origin=(200, 300, 500)))
scene.render(x_range=(-1000, 1000),
             y_range=(-1000, 1000))
