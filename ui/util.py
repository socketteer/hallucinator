from dataclasses import dataclass, asdict, field, make_dataclass, fields
from enum import Enum
from inspect import signature
from pprint import pprint
from typing import Tuple, get_args, get_origin

import numpy as np
import tkinter as tk


# Returns {param:default} and {param:type} for the params of a function or data structure
from ui import controls
def get_param_info_func(func):
    return {name: param.default for name, param in signature(func).parameters.items()}, \
           {name: param.annotation for name, param in signature(func).parameters.items()}


def get_param_info_dataclass(DataClass):
    return {field.name: field.default for field in fields(DataClass)}, \
           {field.name: field.type for field in fields(DataClass)},


generic_types = {
    bool: (bool, np.bool),
    int: (int, np.integer),
    float: (float, np.floating),
    complex: (complex, np.complexfloating),
    str: (str, np.str),
    list: (tuple, list, np.ndarray),
    Enum: (Enum,)
}
# Returns the builtin type corresponding to the given type. If it is a list, it also returns the types in the list
def convert_to_builtin(type_to_convert):
    # If something like typing.Tuple[int, int], change it to Tuple
    subtypes = None
    if get_origin(type_to_convert) is not None:
        subtypes = get_args(type_to_convert)
        type_to_convert = get_origin(type_to_convert)

    for builtin_type, corresponding_types in generic_types.items():
        if issubclass(type_to_convert, corresponding_types):
            return builtin_type, subtypes

    raise ValueError(f"No builtin for {type_to_convert}")


def build_dataclass(name, param_defaults, param_annotations):
    dataclass_params = [
        (name, param_annotations[name], field(default=param_defaults[name]))
        for name in param_defaults.keys()
    ]
    return make_dataclass(name, dataclass_params)


def build_dataclass_for_function(func, name=None):
    param_defaults, param_annotations = get_param_info_func(func)
    if name is None:
        name = func.__name__.title()
    DataClass = build_dataclass(name, param_defaults, param_annotations)

    return DataClass()



def test():
    def test_func(a: int = 1, b: str = "Test", c: bool = False):
        print(a, b, c)

    dc = build_dataclass_for_function(test_func)
    print(dc)
    print(test_func(**asdict(dc)))
    pprint(get_param_info_dataclass(dc))


if __name__ == "__main__":
    test()


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



