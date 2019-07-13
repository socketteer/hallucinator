import sys

sys.path.append('../ikonal')
import ikonal

topdown_gradient = lambda x, y: (x, y, -y)

conditions = (lambda x, y: y < x,
              lambda x, y: y > x ** 2 - 4)

gradient_along_path = ikonal.conditional_region(f=topdown_gradient,
                                                conditions=conditions,
                                                x_range=(-5, 5),
                                                y_range=(-5, 5),
                                                density=10)

gradient_image = ikonal.set_to_gradient(points=gradient_along_path,
                                        x_range=(-5, 5),
                                        y_range=(-5, 5),
                                        black_ref=-5,
                                        white_ref=5,
                                        resolution=20,
                                        default=ikonal.BLACK)

# ikonal.render_from_array(gradient_image)
ikonal.save_img(gradient_image, 'conditional')
