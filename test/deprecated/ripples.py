import sys
sys.path.append('../hallucinator')
import hallucinator
import math
import operator
import numpy as np

f = lambda u: math.sin(100 * u / (2*np.pi)) / u
source1 = hallucinator.wave_2(f, v=2, source=(3, 0), falloff=0.5)
source2 = hallucinator.wave_2(f, v=2, source=(-3, 0), falloff=0.5)
'''source3 = hallucinator.wave_2(f, v=50, source=(0, 0))
source4 = hallucinator.wave_2(f, v=50, source=(1, 0))
source5 = hallucinator.wave_2(f, v=50, source=(2, 0))'''
#source6 = hallucinator.wave_2(f, v=50, source=(1, 0))
#source7 = hallucinator.wave_2(f, v=50, source=(2, 0))
#source8 = hallucinator.wave_2(f, v=50, source=(3, 0))
#source9 = hallucinator.wave_2(f, v=50, source=(9, 0))

superposition = lambda x, y, t: tuple(map(operator.add, source1(x, y, t), source2(x, y, t)))
'''superposition2 = lambda x, y, t: tuple(map(operator.add, superposition(x, y, t), source3(x, y, t)))
superposition3 = lambda x, y, t: tuple(map(operator.add, superposition2(x, y, t), source4(x, y, t)))
superposition4 = lambda x, y, t: tuple(map(operator.add, superposition3(x, y, t), source5(x, y, t)))'''
#superposition5 = lambda x, y, t: tuple(map(operator.add, superposition4(x, y, t), source6(x, y, t)))
#superposition6 = lambda x, y, t: tuple(map(operator.add, superposition5(x, y, t), source7(x, y, t)))
#superposition7 = lambda x, y, t: tuple(map(operator.add, superposition6(x, y, t), source8(x, y, t)))
#superposition8 = lambda x, y, t: tuple(map(operator.add, superposition7(x, y, t), source9(x, y, t)))


hallucinator.wave_2_gradient_video(superposition,
                                   t_range=(0, 10),
                                   x_range=(-10, 10),
                                   y_range=(-10, 10),
                                   resolution=10,
                                   white_ref=2.0,
                                   black_ref=-2.0,
                                   fps=10,
                                   filename='ripples_falloff_8')
