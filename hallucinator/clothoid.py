import hallucinator as hl
import math


def clothoid(scene, plot_range=(0, 50), resolution=30, scale=1, center=(0, 0), phase=0):
    complex_zp = hl.complex_zp(scale, center, phase)
    endpoints = hl.plot_phase_integral(pattern=complex_zp, plot_range=plot_range, resolution=resolution, scene=scene)
    return endpoints


# returns array with clothoid image
def plot_clothoid(padding=0, plot_range=(0, 50), resolution=20, scale=1, center=(0, 0), phase=0):
    scene = hl.MonochromeScene()

    endpoints = clothoid(scene, plot_range=plot_range, resolution=resolution, scale=scale, center=center, phase=phase)

    x_values = [e[0] for e in endpoints]
    y_values = [e[1] for e in endpoints]

    max_x = int(math.ceil(max(x_values)))
    min_x = int(math.floor(min(x_values)))
    max_y = int(math.ceil(max(y_values)))
    min_y = int(math.floor(min(y_values)))

    clothoid_arr = scene.render_scene(x_range=(min_x - padding, max_x + padding),
                                      y_range=(min_y - padding, max_y + padding),
                                      resolution=10, densities=15, projection_type=hl.Projections.ORTHO)

    return clothoid_arr
