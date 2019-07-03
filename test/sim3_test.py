import obj3
import scene
import simulate


def transition_rule(frame):
    next_frame = scene.Scene3()
    for obj in frame.objects:
        if obj.species == 'box':
            next_frame.add_object(obj.rotate(50, axis='Z'))
        else:
            next_frame.add_object(obj)
    return next_frame


init_frame = scene.Scene3()
init_frame.add_object(obj3.box(200, 200, 200, (0, 0, 500)))
init_frame.add_object(obj3.axes((-5000, 5000), (-5000, 5000), (-5000, 5000), origin=(200, 300, 500)))


width = 2000
height = 2000
FPS = 10
seconds = 3

simulate.generate_video_3(frame=init_frame,
                          transition_rule=transition_rule,
                          filename='rotate3', width=width, height=height,
                          x_range=(-1000, 1000), y_range=(-1000, 1000),
                          pov=(0, 0, 0), z_scale=0.005,
                          FPS=FPS, seconds=seconds)
