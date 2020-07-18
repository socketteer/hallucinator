from enum import Enum
from inspect import signature
from typing import Tuple, get_args, get_origin

import numpy as np
import tkinter as tk


# Returns {param:default} and {param:type} for the params of a function or data structure
from ui import controls


def get_param_info(func):
    return {name: param.default for name, param in signature(func).parameters.items()}, \
           {name: param.annotation for name, param in signature(func).parameters.items()}


generic_types = {
    int: (int, np.integer),
    float: (float, np.floating),
    complex: (complex, np.complexfloating),
    bool: (bool, np.bool),
    str: (str, np.str),
    list: (tuple, list, np.ndarray),
    Enum: (Enum,)
}
def convert_to_builtin(type_to_convert):
    for builtin_type, corresponding_types in generic_types.items():
        # If something like typing.Tuple[int, int], change it to tuple. TODO Handle
        if get_origin(type_to_convert) is not None:
            type_to_convert = get_origin(type_to_convert)
        # Otherwise check the generic types dict
        if issubclass(type_to_convert, corresponding_types):
            return builtin_type

    raise ValueError()



# tkinter_types = {
#     int: tk.IntVar,
#     float: tk.DoubleVar,
#     complex: tk.DoubleVar,
#     bool: (bool, np.bool),
#     Enum: tk.StringVar,
# }
#
# input_types = {
#     ((float, np.floating), "spinbox"),  # Includes float32,64
#     ((complex, np.complexfloating), "spinbox"),  # Includes complex64,128
#     ((int, np.integer), "spinbox"),  # Includes uints
#     (Enum, "dropdown"),
#     ((bool, np.bool), "checkbox")
# }



