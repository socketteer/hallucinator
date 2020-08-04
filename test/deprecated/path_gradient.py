import sys
sys.path.append('../hallucinator')
import hallucinator

topdown_discrete = lambda x, y: (x, y, -1 if y < 0 else 1)
topdown_gradient = lambda x, y: (x, y, -y)

path = lambda p: (p, p)
p_range = [-3, 3]
gradient_along_path = hallucinator.path_region(f=topdown_gradient,
                                               path=path,
                                               p_range=p_range,
                                               density=5)

gradient_image = hallucinator.set_to_gradient(points=gradient_along_path,
                                              x_range=(-5, 5),
                                              y_range=(-5, 5),
                                              black_ref=-3,
                                              white_ref=3,
                                              default=hallucinator.BLUE)

# hallucinator.render_from_array(gradient_image)
hallucinator.save_img(gradient_image, 'path_grad_test0')
