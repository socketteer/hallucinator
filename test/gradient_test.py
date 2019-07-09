import sys
sys.path.append('../ikonal')
import ikonal
import numpy as np
import math

f = lambda x, y: math.sin(500 * math.sqrt(x**2 + y**2) / (2 * np.pi))

arr = ikonal.phasegrid(f, (-5, 5), (-5, 5), resolution=100)

grad = ikonal.arr_to_gradient(arr, black_ref=-2.0, white_ref=2.0)

ikonal.render_from_array(grad)
