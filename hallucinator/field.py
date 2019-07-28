import hallucinator as hl


#TODO 2d and 3d?
def slope_field(points,
                     arrow_length = 1,
                     arrow_head_length = 0.2):
    """
    Draw an arrow with slope f'(x, y) at each point (x, y) in points
    :param points: (x, y, f'(x, y))
    :return:
    """
    field = hl.MonochromeScene()
    for point in points:
        field.add_object(hl.arrow(p0=point[0:2],
                                  direction=point[2],
                                  length=arrow_length,
                                  head_length=arrow_head_length),
                         name='{0}{1}'.format(point[0], point[1]))

    return field
