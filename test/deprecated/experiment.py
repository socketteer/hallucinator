import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math
import numpy as np

frequency = 75
amplitude = 1

f = lambda u: amplitude * math.sin(frequency * u / (2 * np.pi))

center1 = (0, 0.3)
center2 = (0, -0.3)

source1 = hl.wave_2(f=f, v=1, source=center1, falloff=0)
source2 = hl.wave_2(f=f, v=1, source=center2, falloff=0)

superposition = hl.superposition(source1, source2)

scene = hl.GrayscaleScene()

wave = hl.ParaObject2(f=superposition,
                      region_type="surface",
                      region_params={"a_range": (-10, 10),
                                     "b_range": (-10, 10),
                                     "a_name": 'x',
                                     "b_name": 'y'},
                      species='wave_superposition')

scene.add_object(wave.rotate(theta=math.pi / 2, p=(0, 0)), name='wave')

hl._deprecated_video(frame_func=lambda t: scene.render_scene(params={'wave': {'t': t}},
                                                             x_range=(-12, 12),
                                                             y_range=(-12, 12),
                                                             resolution=20,
                                                             density=5,
                                                             white_ref=2.0,
                                                             black_ref=-2.0,
                                                             display=False,
                                                             default=hl.GRAY),
                     filename='two_slit2',
                     t_range=(1, 5),
                     FPS=10)
