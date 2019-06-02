import render
import numpy as np

img = np.zeros((400, 400), dtype=np.bool)
for x in range(400):
    for y in range(400):
        img[-y, x] = 1 if y == x**2 else 0

img = render.binary_to_bichrom(img)
render.render_from_array(img)
