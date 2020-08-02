import hallucinator as hl
import numpy as np


def camscene(scene,
             camera_pos=(0, 0, 0),
             camera_rotation=(0, 0, 0),
             render_density=100,
             projection_type='weak',
             styles='uniform',
             x_range=(-5, 5),
             y_range=(-5, 5),
             resolution=200):
    camera_position = np.matmul(hl.translate_3(camera_pos), hl.IDENTITY4)
    #camera_position = np.matmul(hl.rotate_about_3(camera_rotation[0], axis=(1, 0, 0), p=camera_pos), camera_position)
    #camera_position = np.matmul(hl.rotate_about_3(camera_rotation[1], axis=(0, 1, 0), p=camera_pos), camera_position)
    #camera_position = np.matmul(hl.rotate_about_3(camera_rotation[2], axis=(0, 0, 1), p=camera_pos), camera_position)

    return scene.render_scene(x_range=x_range,
                              y_range=y_range,
                              resolution=resolution,
                              camera_position=camera_position,
                              projection_type=projection_type,
                              styles=styles,
                              density=render_density,
                              foreground=hl.WHITE,
                              background=hl.BLACK,
                              display=False)