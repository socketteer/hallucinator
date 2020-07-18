import math
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider

from hallucinator import xy_plane, perspective_zp, perspective_plane


def plot_images(images, titles=None):
    image_plots = create_plots_grid(num_plots=len(images), titles=titles)
    for i in range(len(images)):
        image_plots[i].imshow(images[i], cmap=cm.gray, aspect="auto")
    plt.show()


def create_plots_grid(num_plots, titles=None, plot_cell=None):
    if num_plots % 4 == 0 or num_plots > 9:
        rows = max(1, math.ceil(num_plots / 4))
        cols = 4
    else:
        rows = max(1, math.ceil(num_plots / 3))
        cols = min(num_plots, 3)

    plot_cell = plot_cell if plot_cell else gridspec.GridSpec(1, 1)[0]
    hspace = 0.2 if titles else 0.01
    plot_grid = gridspec.GridSpecFromSubplotSpec(rows, cols, plot_cell, wspace=0.01, hspace=hspace)
    image_plots = []
    for i in range(num_plots):
        ax = plt.subplot(plot_grid[i])
        ax.axis("off")
        if titles and len(titles) > i:
            ax.set_title(titles[i])
        image_plots.append(ax)

    return image_plots


# Slider_params = ["param_name", min, max]
# Caller must set slider.on_change(update_func) for each slider themselves
def create_slider_plots(*, controls_cell, slider_params):
    num_sliders = len(slider_params)
    slider_grid = gridspec.GridSpecFromSubplotSpec(num_sliders, 1, controls_cell, wspace=0.01, hspace=1)
    sliders = []
    for i, params in enumerate(slider_params):
        slider_ax = plt.subplot(slider_grid[i])

        slider = Slider(slider_ax,
                        label=params[0],
                        valmin=params[1],
                        valmax=params[2],
                        valinit=(params[2]+params[1])/2)
        sliders.append(slider)

    return sliders


# def create_multiplot(num_images=1, controls=False):
#     fig = plt.figure()
#     if controls:
#         rows = 2
#         parent_grid = gridspec.GridSpec(2, 1, wspace=0.025, hspace=0.05, left=0.05, bottom=0.05, right=0.95, top=0.95,
#                                         height_ratios=[10, 1])
#         controls_cell = parent_grid[1]
#     else:
#         parent_grid = gridspec.GridSpec(1, 1, wspace=0.025, hspace=0.05, left=0.05, bottom=0.05, right=0.95, top=0.95)
#     plots_cell = parent_grid[0]
#
#     return create_image_plots(plots_cell, num_images)


def create_interactive_plot(*, images_func, num_images, slider_params, titles=None, cmap=cm.gray):
    fig = plt.figure()

    spacing = dict(wspace=0.025, hspace=0.05, left=0.05, bottom=0.05, right=0.95, top=0.95)
    parent_grid = gridspec.GridSpec(2, 1,  **spacing, height_ratios=[10, 1])
    image_plots = create_plots_grid(num_plots=num_images, titles=titles, plot_cell=parent_grid[0])
    sliders = create_slider_plots(controls_cell=parent_grid[1], slider_params=slider_params)

    def update_func(val):
        slider_vals = {slider_param[0]: slider.val for slider_param, slider in zip(slider_params, sliders)}
        images = images_func(**slider_vals)
        for image, image_plot in zip(images, image_plots):
            image_plot.imshow(image, cmap=cmap, aspect="auto")
    for slider in sliders:
        slider.on_changed(update_func)

    # Render for the first time
    update_func(0)
    plt.show()


##############################################################################
# TESTS
##############################################################################

def test_create_plots_grid(num_images=9):
    def squiggle_xy(a, b, c, d):
        i = np.arange(0.0, 2*np.pi+0.05, 0.05)
        return np.sin(i*a)*np.cos(i*b), np.sin(i*c)*np.cos(i*d)

    plots = create_plots_grid(num_images)
    for i, ax in enumerate(plots):
        a = i // 4 + 1
        b = i % 4 + 1
        c, d = 2, 3
        ax.plot(*squiggle_xy(a, b, c, d))

    plt.show()


def test_plot_images():
    def example_image(i):
        xy = xy_plane(value_range=(-10, 10), resolution=100)
        persp_xy = perspective_plane(xy, p=[0, 0, i*10])
        zp = perspective_zp(persp_xy)
        return zp

    num_images = 6
    plot_images(images=[example_image(i) for i in range(num_images)]),
                # titles=[f"title {i}" for i in range(num_images)])


def test_create_interactive_plot():
    xy = xy_plane(value_range=(-10, 10), resolution=300)
    example_params = dict(
        images_func=lambda x, y, z: [
            perspective_zp(perspective_plane(xy, p=[x, y, z])),
            perspective_zp(perspective_plane(xy, p=[0, 0, 50])),
            perspective_zp(perspective_plane(xy, p=[x, y, z]) - perspective_plane(xy, p=[0, 0, -50]))
        ],
        num_images=3,
        titles=[
            "zp: x,y,z",
            "zp: 0,0,-50",
            "combined"
        ],
        slider_params=[
            ["x", -10, 10],
            ["y", -10, 10],
            ["z", 0, 100]
        ]
    )
    create_interactive_plot(**example_params)


if __name__ == "__main__":
    # test_create_plots_grid()
    # test_plot_images()
    test_create_interactive_plot()


