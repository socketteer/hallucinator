import hallucinator as hl

clothoid = hl.plot_clothoid(padding=5, plot_range=(0, 400), resolution=6)
hl.render_from_array(clothoid)
