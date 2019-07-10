import sys
sys.path.append('../ikonal')
import ikonal

f = lambda y: 3 / (2 * y ** 2 + 1)
wf = ikonal.wave_2(f, v=2, source=(1, 1))
print('wf(0, 0, 0): ', wf(0, 0, 0))
print('wf(0, 0, 1): ', wf(0, 0, 1))
print('wf(0, 1, 1): ', wf(0, 1, 1))
print('wf(1, 0, 1): ', wf(1, 0, 1))

frame1 = ikonal.gradient_frame(f=wf,
                               t=0,
                               white_ref=4,
                               black_ref=0,
                               x_range=(-5, 5),
                               y_range=(-5, 5),
                               resolution=20)
frame2 = ikonal.gradient_frame(f=wf,
                               t=1,
                               white_ref=4,
                               black_ref=0,
                               x_range=(-5, 5),
                               y_range=(-5, 5),
                               resolution=20)

ikonal.render_from_array(frame1)
ikonal.render_from_array(frame2)

ikonal.wave_2_gradient_video(wf,
                             t_range=(0, 5),
                             x_range=(-5, 5),
                             y_range=(-5, 5),
                             resolution=5,
                             white_ref=4,
                             black_ref=0,
                             fps=4,
                             filename='propw2d')
