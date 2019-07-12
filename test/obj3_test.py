import ikonal

frame = scene.Scene3()
box = obj3.box(200, 200, 200, (0, 0, 500))
frame.add_object(box)
frame.add_object(box.rotate(30, axis='Y'))
frame.add_object(box.rotate(90, axis='Y'))
frame.add_object(box.rotate(150, axis='Y'))


frame.add_object(ikonal.axes_3((-5000, 5000), (-5000, 5000), (-5000, 5000), origin=(200, 300, 500)))
frame.lazy_render(x_range=(-1000, 1000),
                  y_range=(-1000, 1000))
