import sys
sys.path.append('../hallucinator')
import hallucinator

f = lambda y: 3 / (2 * y ** 2 + 1)
wf = hallucinator.wave(f, 2)
print('wf(0, 0): ', wf(0, 0))
print('wf(0, 1): ', wf(0, 1))
print('wf(1, 0): ', wf(1, 0))
hallucinator.plot_profile(f=wf,
                          t=0,
                          x_range=(-5, 5),
                          y_range=(-5, 5),
                          density=50)


hallucinator.wave_video(f=wf,
                        t_range=(-4, 4),
                        x_range=(-5, 5),
                        y_range=(-2, 5),
                        FPS=10,
                        density=50)
