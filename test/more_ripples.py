import sys
sys.path.append('../hallucinator')
import hallucinator
import operator


f = lambda y: 3 / (2 * y ** 2 + 1)
source1 = hallucinator.wave_2(f, v=3, source=(2.5, 0), falloff=0.5, starttime=1)
source2 = hallucinator.wave_2(f, v=3, source=(2, 0), falloff=0.5, starttime=1.5)
source3 = hallucinator.wave_2(f, v=3, source=(1, 0), falloff=0.5, starttime=2)
source4 = hallucinator.wave_2(f, v=3, source=(0, 0), falloff=0.5, starttime=2.5)
source5 = hallucinator.wave_2(f, v=3, source=(-1, 0), falloff=0.5, starttime=3)
source6 = hallucinator.wave_2(f, v=3, source=(-1.5, 0), falloff=0.5, starttime=3.5)
source7 = hallucinator.wave_2(f, v=3, source=(-1.5, 0), falloff=0.5, starttime=4)
source8 = hallucinator.wave_2(f, v=3, source=(-1.5, 0), falloff=0.5, starttime=4.5)
source9 = hallucinator.wave_2(f, v=3, source=(-1.5, 0), falloff=0.5, starttime=5)

superposition = lambda x, y, t: tuple(map(operator.add, source1(x, y, t), source2(x, y, t)))
superposition2 = lambda x, y, t: tuple(map(operator.add, superposition(x, y, t), source3(x, y, t)))
superposition3 = lambda x, y, t: tuple(map(operator.add, superposition2(x, y, t), source4(x, y, t)))
superposition4 = lambda x, y, t: tuple(map(operator.add, superposition3(x, y, t), source5(x, y, t)))
superposition5 = lambda x, y, t: tuple(map(operator.add, superposition4(x, y, t), source6(x, y, t)))
superposition6 = lambda x, y, t: tuple(map(operator.add, superposition5(x, y, t), source7(x, y, t)))
superposition7 = lambda x, y, t: tuple(map(operator.add, superposition6(x, y, t), source8(x, y, t)))
superposition8 = lambda x, y, t: tuple(map(operator.add, superposition7(x, y, t), source9(x, y, t)))

hallucinator.video(frame_func=lambda t: hallucinator.gradient_frame(f=superposition8,
                                                                    p={'t': t},
                                                                    x_range=(-5, 5),
                                                                    y_range=(-5, 5),
                                                                    resolution=10,
                                                                    white_ref=10.0,
                                                                    black_ref=0),
                   filename='doesthisstillwork2',
                   t_range=(0, 5.5),
                   FPS=10)


