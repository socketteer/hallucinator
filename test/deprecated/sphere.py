import sys

sys.path.append('../hallucinator')
import hallucinator as hl
import math


def rotating_sphere(t):
    speed = 0.7
    frame = hl.MonochromeScene()
    vector = hl.np.array([1, 0, 0])
    frame.add_object(
        hl.sphere(center=(10, 0, 30), radius=10).rotate(theta=math.pi / 2,
                                                        axis=(0, 1, 0), p=(10, 0, 30)).rotate(theta=t * speed,
                                                                                              axis=vector,
                                                                                              p=(10, 0, 30)).project(
            method='weak'),
        name="sphere")

    frame.add_object(
        hl.sphere(center=(10, 0, 30), radius=7).rotate(theta=math.pi / 2,
                                                        axis=(0, 1, 0), p=(10, 0, 30)).rotate(theta=-t * speed,
                                                                                              axis=vector,
                                                                                              p=(10, 0, 30)).project(
            method='weak'),
        name="sphere2")

    return frame.render_scene(x_range=(-10, 50),
                              y_range=(-30, 30),
                              resolution=20,
                              density=5,
                              style='wireframe',
                              region_params={'a_spacing': 2,
                                             'b_spacing': 2},
                              foreground=(51, 255, 255),
                              background=(112, 50, 50),
                              display=False)


hl._deprecated_video(frame_func=lambda t: rotating_sphere(t),
                     filename='sphere_in_sphere',
                     t_range=(0, 10),
                     FPS=20)
