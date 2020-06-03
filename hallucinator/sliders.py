import math

from matplotlib import cm

import hallucinator as hl
from hallucinator.perspective import xy_plane, perspective_plane, perspective_zp
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


xy = xy_plane(value_range=(-10, 10))
persp_xy = perspective_plane(xy)
zp = perspective_zp(persp_xy)

# plt.imshow(zp, cmap=cm.gray)
# plt.show()

#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# fig.subplots_adjust(left=0.25, bottom=0.25)
# min0 = 0
# max0 = 25000

# im1 = ax.imshow(xy)
# fig.colorbar(im1)
#
# axcolor = 'lightgoldenrodyellow'
# axmin = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
# axmax  = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
#
# smin = Slider(axmin, 'Min', 0, 30000, valinit=min0)
# smax = Slider(axmax, 'Max', 0, 30000, valinit=max0)
#
# def update(val):
#     im1.set_clim([smin.val, smax.val])
#     fig.canvas.draw()
# smin.on_changed(update)
# smax.on_changed(update)
#
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider


def show_image(ax, i):
    xy = xy_plane(value_range=(-10, 10), resolution=100*i+500)
    persp_xy = perspective_plane(xy, p=[0, 0, i])
    zp = perspective_zp(persp_xy)
    ax.imshow(zp, cmap=cm.gray, aspect='auto')

def update(_):
    pass

# # Half width of the graph x-axis
# x_axis = 4*np.pi
# # x_axis offset
# x_offset = 0
# # Half height of the graph y-axis
# y_axis = 8
# # y_axis offset
# y_offset = -1

fig = plt.figure()
parent_grid = gridspec.GridSpec(2, 1, wspace=0.025, hspace=0.05, left=0.1, bottom=0.1, right=0.95, top=0.95,
                                height_ratios=[10, 1])
plots_cell = parent_grid[0]
controls_cell = parent_grid[1]

# Plots
plot_count = 4

if plot_count == 4:
    rows = 2
    cols = 2
else:
    rows = max(1, math.ceil(plot_count / 3))
    cols = min(plot_count, 3)

plot_grid = gridspec.GridSpecFromSubplotSpec(rows, cols, plots_cell, wspace=0.01, hspace=0.01)
plots = []
for i in range(plot_count):
    ax = plt.subplot(plot_grid[i])
    ax.axis("off")
    plots.append(ax)

for i, p in enumerate(plots):
    show_image(p, i)

# plt.tight_layout()

# plt.subplots_adjust(wspace=0, hspace=0)
# for i, pt in enumerate(plots):
#     show_image(pt, i)

# Sliders
slider_count = 5
slider_grid = gridspec.GridSpecFromSubplotSpec(slider_count, 1, controls_cell, wspace=0.01, hspace=1)
sliders = []
for i in range(slider_count):
    sliderax = plt.subplot(slider_grid[i])
    slider = Slider(sliderax, "Test {}".format(i), 0.1, 8.0, valinit=2, valstep=0.01)
    slider.on_changed(update)
    sliders.append(slider)

plt.show()

