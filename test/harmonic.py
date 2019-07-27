import sys
sys.path.append('../hallucinator')
import hallucinator

f = lambda y: 3 / (2 * y ** 2 + 1)
wf = hallucinator.harmonic(amplitude=1, wavelength=3, frequency=5)

hallucinator.plot_profile(f=wf,
                          t=0,
                          x_range=(-5, 5),
                          y_range=(-5, 5),
                          background=hallucinator.BLUE,
                          density=100)


'''hallucinator.wave_video(f=wf,
                  t_range=(-4, 4),
                  x_range=(-5, 5),
                  y_range=(-5, 5),
                  background=hallucinator.RED,
                  FPS=15,
                  density=100,
                  filename='harmonic')'''
