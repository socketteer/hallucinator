import sys

sys.path.append('../hallucinator')
import hallucinator


def scene_at_t(t):
    frame = hallucinator.MonochromeScene()
    frame.add_object(hallucinator.plane_section(p0=(t * 20 - 50, 0, 0),
                                                v1=(0, 1, 0),
                                                v2=(1, 0, 1),
                                                a_range=(-100, 100),
                                                b_range=(0, 200)).project(method='weak'), "plane")

    return frame.render_scene(x_range=(-30, 30),
                              y_range=(-30, 30),
                              resolution=20,
                              density=50,
                              foreground=hallucinator.WHITE,
                              background=hallucinator.BLACK,
                              display=False)


hallucinator.video(frame_func=lambda t: scene_at_t(t),
                   filename='plane_test_3',
                   t_range=(0, 10),
                   FPS=20)
