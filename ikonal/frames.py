import ikonal





def regional_gradient_frame(f, p, region, x_range, y_range, resolution=5, white_ref=1.0,
                            black_ref=-1.0, default=ikonal.BLUE, backdrop='new'):
    """

    :param f:
    :param p: dictionary of additional parameters (such as t)
    :param region:
    :param x_range:
    :param y_range:
    :param resolution:
    :param white_ref:
    :param black_ref:
    :param default:
    :param backdrop:
    :return: array with shape (x_range, y_range)*resolution of (gradient, gradient, gradient)
    """
    #TODO this should use AT instead
    gradient_points = region(lambda a, b: f(a, b, **p))
    gradient_image = ikonal.set_to_gradient(points=gradient_points,
                                            x_range=x_range,
                                            y_range=y_range,
                                            black_ref=black_ref,
                                            white_ref=white_ref,
                                            resolution=resolution,
                                            default=default,
                                            canv=backdrop)

    return gradient_image


def gradient_frame(f, p, x_range, y_range, white_ref=-1.0, black_ref=1.0, resolution=5):
    """
    :param f:
    :param p: dictionary of additional parameters (such as t)
    :param x_range:
    :param y_range:
    :param white_ref:
    :param black_ref:
    :param resolution:
    :return: array with shape (x_range, y_range)*resolution of (gradient, gradient, gradient)
    """

    phasegrid = ikonal.phasegrid(lambda a, b: f(a, b, **p)[2],
                                 x_range=x_range,
                                 y_range=y_range,
                                 resolution=resolution)
    grad = ikonal.arr_to_gradient(phasegrid,
                                  white_ref=white_ref,
                                  black_ref=black_ref)
    return grad
