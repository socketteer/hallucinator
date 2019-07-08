import sys
sys.path.append('../ikonal')
import ikonal

f = lambda y: 3 / (2 * y ** 2 + 1)
wf = ikonal.harmonic(amplitude=1, wavelength=3, frequency=5)

ikonal.plot_profile(f=wf,
                    t=0,
                    x_range=(-5, 5),
                    y_range=(-5, 5),
                    background=ikonal.BLUE,
                    density=100)


'''ikonal.wave_video(f=wf,
                  t_range=(-4, 4),
                  x_range=(-5, 5),
                  y_range=(-5, 5),
                  background=ikonal.RED,
                  FPS=15,
                  density=100,
                  filename='harmonic')'''
