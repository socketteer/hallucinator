import wave

f = lambda y: (y, 3 / (2 * y ** 2 + 1))
wf = wave.wave(f, 2)
print(wf(0, 0))
print(wf(0, 1))
print(wf(1, 0))
wave.plot_profile(f=wf,
                  t=0,
                  x_range=(-5, 5),
                  y_range=(-5, 5),
                  density=50)
