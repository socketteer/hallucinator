import sys

sys.path.append('../hallucinator')
import hallucinator
import math
import numpy as np


frequency = 75
amplitude = 1

f = lambda u: amplitude * math.sin(frequency * u / (2 * np.pi))

center1 = (0, 0.3)
center2 = (0, -0.3)


source1 = hallucinator.wave_2(f=f, v=1, source=center1, falloff=0)
source2 = hallucinator.wave_2(f=f, v=1, source=center2, falloff=0)

superposition = hallucinator.superposition(source1, source2)


rect_region = lambda fu: hallucinator.surface_region(f=fu,
                                                     x_range=(1, 5),
                                                     y_range=(-7, 7),
                                                     density=10)

scene = hallucinator.MonochromeScene()
scene.add_object(hallucinator.ripple(num_crests=3, wavelength=1 / 3, center=center1))
scene.add_object(hallucinator.ripple(num_crests=3, wavelength=1 / 3, center=center2))
canv = scene.render_scene(x_range=(-10, 10),
                          y_range=(-10, 10),
                          resolution=20,
                          density=5,
                          foreground=hallucinator.WHITE,
                          background=hallucinator.GRAY,
                          display=False)

hallucinator.video(frame_func=lambda t: hallucinator.regional_gradient_frame(f=superposition,
                                                                             p={'t': t},
                                                                             region=rect_region,
                                                                             x_range=(-10, 10),
                                                                             y_range=(-10, 10),
                                                                             resolution=20,
                                                                             white_ref=2.0,
                                                                             black_ref=-2.0,
                                                                             backdrop=canv),
                   filename='two_slit2',
                   t_range=(1, 10),
                   FPS=20)
