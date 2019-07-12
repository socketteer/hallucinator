import sys
sys.path.append('../ikonal')
import ikonal

topdown_discrete = lambda x, y: (x, y, -1 if y < 0 else 1)
topdown_gradient = lambda x, y: (x, y, -y)

path = lambda p: (p, p)
p_range = [-3, 3]
gradient_along_path = ikonal.path_region(f=topdown_gradient,
                                         path=path,
                                         p_range=p_range,
                                         density=5)

gradient_image = ikonal.set_to_gradient(points=gradient_along_path,
                                        x_range=(-5, 5),
                                        y_range=(-5, 5),
                                        black_ref=-3,
                                        white_ref=3,
                                        default=ikonal.BLUE)

# ikonal.render_from_array(gradient_image)
ikonal.save_img(gradient_image, 'path_grad_test0')
