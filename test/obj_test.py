import sys

sys.path.append('../ikonal')
import ikonal
import math

scene = ikonal.Scene()

scene.add_object(ikonal.vector(p1=(0, 20), p2=(20, 20)))
# scene.add_object(ikonal.vector(p1=(0, 20), p2=(20, 20)).rotate(math.pi/2))

# scene.add_object(ikonal.vector(p1=(0, 20), p2=(20, 20)).rotate(math.pi))
# scene.add_object(ikonal.vector(p1=(0, 20), p2=(20, 20)).rotate(2/3*math.pi))
scene.add_object(ikonal.vector(p1=(0, 20), p2=(20, 20)).rotate(math.pi / 3, (0, 20)))
scene.add_object(ikonal.vector(p1=(0, 20), p2=(20, 20)).rotate(math.pi / 2, (20, 20)))

scene.add_object(ikonal.rectangle(h=20, w=100, p0=(5, 10)))
scene.add_object(ikonal.circle(r=10, c=(-20, -20)))
scene.add_object(ikonal.circle(r=10, c=(-20, -20)).scale(2, 2))
scene.add_object(ikonal.circle(r=10, c=(-20, -20)).scale(0.5, 1, p=(-20, -20)))

scene.add_object(ikonal.square(w=10, p0=(30, -20)))
scene.add_object(ikonal.ripple(num_crests=10, wavelength=2, center=(0, 0)))

scene.add_object(ikonal.axes((-50, 50), (-50, 50), origin=(0, 0)))

scene.render_scene(x_range=(-40, 40),
                   y_range=(-40, 40),
                   resolution=20,
                   density=2,
                   foreground=ikonal.WHITE,
                   background=ikonal.BLACK,
                   display=True)
