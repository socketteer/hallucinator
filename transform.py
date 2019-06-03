import numpy as np
import objects


def transform(operator, operand):
    if isinstance(operand, objects.Group):
        new = objects.Group()
        for component in operand.components:
            new.add_component(transform(operator, component))
        return new
    elif isinstance(operand, objects.ParaObject):
        return objects.ParaObject(lambda x: operator(operand.func(x)), operand.path, operand.num_points)
    elif isinstance(operand, function):
        return lambda x: operator(operand(x))
