import hallucinator as hl

scene = hl.MonochromeScene()
scene.add_object(hl.rectangle(h=30, w=40), "rect")

rect_arr = scene.render_scene(x_range=(-50, 50), y_range=(-50, 50), densities=1, projection_type=hl.Projections.ORTHO)
hl.render_from_array(rect_arr)