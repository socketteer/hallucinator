import sys

sys.path.append('../hallucinator')
import hallucinator

canvas = hallucinator.MonochromeScene()
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(-70, -10)), "axes1")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(-70, 40)), "axes2")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(-70, -60)), "axes3")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(-20, -10)), "axes4")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(-20, 40)), "axes5")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(-20, -60)), "axes6")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(30, -10)), "axes7")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(30, 40)), "axes8")
canvas.add_object(hallucinator.axes((0, 40), (0, 40), origin=(30, -60)), "axes9")

background = canvas.render_scene(x_range=(-80, 80),
                                 y_range=(-80, 80),
                                 resolution=10,
                                 density=1,
                                 foreground=hallucinator.RED,
                                 background=hallucinator.BLACK,
                                 display=False)

frame = hallucinator.MonochromeScene()
# hallucinator.render_from_array(background)
frame.add_object(hallucinator.polygon(30, 3).translate(-60, 40), "triangle")
frame.add_object(hallucinator.polygon(25, 4).translate(-60, -10), "square")
frame.add_object(hallucinator.polygon(20, 5).translate(-60, -60), "pentagon")
frame.add_object(hallucinator.polygon(15, 6).translate(-10, 40), "hexagon")
frame.add_object(hallucinator.polygon(13, 7).translate(-10, -10), "heptagon")
frame.add_object(hallucinator.polygon(11, 8).translate(-10, -60), "octagon")

frame.add_object(hallucinator.polygon(10, 9).translate(45, 40), "enneagon")
frame.add_object(hallucinator.polygon(9, 10).translate(45, -10), "decagon")
frame.add_object(hallucinator.polygon(8, 11).translate(45, -60), "undecagon")

frame.render_scene(x_range=(-80, 80),
                   y_range=(-80, 80),
                   resolution=10,
                   density=2,
                   foreground=hallucinator.WHITE,
                   background=hallucinator.BLACK,
                   backdrop=background,
                   display=True)
