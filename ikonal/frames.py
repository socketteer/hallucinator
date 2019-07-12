import ikonal


def selective_gradient_frame(func, t, path, p_range, density, x_range, y_range, resolution=5, white_ref=1.0,
                             black_ref=-1.0, default=ikonal.BLUE):
    gradient_points = ikonal.phasepath(func=lambda x, y: func(x, y, t),
                                       path=path,
                                       p_range=p_range,
                                       density=density)
    gradient_image = ikonal.set_to_gradient(points=gradient_points,
                                            x_range=x_range,
                                            y_range=y_range,
                                            black_ref=black_ref,
                                            white_ref=white_ref,
                                            resolution=resolution,
                                            default=default)

    return gradient_image


def gradient_frame(f, t, x_range, y_range, white_ref=-1.0, black_ref=1.0, resolution=50):
    phasegrid = ikonal.phasegrid(lambda x, y: f(x, y, t)[2],
                                 x_range=x_range,
                                 y_range=y_range,
                                 resolution=resolution)
    grad = ikonal.arr_to_gradient(phasegrid,
                                  white_ref=white_ref,
                                  black_ref=black_ref)
    return grad
