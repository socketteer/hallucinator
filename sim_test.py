import obj
import scene
import simulate


def transition_rule(frame):
    next_frame = scene.Scene()
    for obj in frame.objects:
        if obj.species == 'circle':
            next_frame.add_object(obj.rotate(10, (0, 0)))
        else:
            next_frame.add_object(obj)
    return next_frame


init_frame = scene.Scene()
init_frame.add_object(obj.circle(50, (100, 100)))
init_frame.add_object(obj.axes((-500, 500), (-500, 500), origin=(0, 0)))

width = 2000
height = 2000
FPS = 3
seconds = 13

simulate.generate_video(frame=init_frame,
                        transition_rule=transition_rule,
                        filename='rotate', width=width, height=height,
                        x_range=(-1000, 1000), y_range=(-1000, 1000),
                        FPS=FPS, seconds=seconds)


