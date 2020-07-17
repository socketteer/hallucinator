import types
from dataclasses import dataclass
from enum import Enum
from inspect import signature
from typing import TypedDict, NamedTuple, Tuple

import numpy as np
import numexpr as ne
import hallucinator as hl
import tkinter as tk

from ui import controls
from ui.util import get_param_info



# TODO Add more
class ColorStyle(Enum):
    GRAYSCALE = "Grayscale"
    HSV = "HSV"
    WHAT = "???"


# TODO Add more
class PlotStyle(Enum):
    CONTOUR = "Contour"
    REAL = "Real"
    IMAGINARY = "Imaginary"


# NamedTuple not mutable
# TypedDict no defaults
# SimpleNamespace no signature
# @dataclass is the way!!!

@dataclass
class ViewSettings:
    style: ColorStyle = ColorStyle.HSV
    plot_type: PlotStyle = PlotStyle.CONTOUR
    value_range: Tuple[int, int] = (-1, 1)
    resolution: int = 500
    example_complex: complex = 1
    autorender: bool = True


class ComputedObject(NamedTuple):
    name: str
    func: types.FunctionType
    params: dict
    param_types: dict

    @classmethod
    def new(cls, name, func):
        param_defaults, param_types = get_param_info(func)
        param_defaults.pop("view_settings")
        return ComputedObject(name=name, func=func, params=param_defaults, param_types=param_types)


class TkComputedObject(ComputedObject):
    tk_vars: dict


class DerivedObject:
    name: str
    operation: Enum
    operands: list



def zoneplate(view_settings: ViewSettings, x: float = 0, y: float = 0):
    center = [x, y]
    xy = hl.xy_plane(value_range=view_settings.value_range, resolution=view_settings.resolution)
    x2y2 = ne.evaluate("sum(((xy-center)*10)**2, axis=2)")
    return x2y2





# self.name = ("Type", string)
# self.x = ("x", float, 0)
#
#
#
#
# checkbox
# dropdown
# textfield
# slider
#
# bool: checkbox
# enum: dropdown
# int, floats: input field, slider?
# string: input field
#
#
# available_shapes = [
#     zoneplate,
#     pinchzone,
# ]
#
# class View:
#     range
#     x, y
#     style
#
# class Shape:
#     name
#     func
#     params = {}
#
# class Derived:
#     name
#     operation
#     operands




#
# class Shape:
#     type, func, name, x, y, scale, conjugate, rotate
#
#
# class FuncOfR(Shape):
#     function_string
#
#     def render():
#         plane = ne.evaluate("...")
#         return ...
#
# class PinchZone(Shape):
#     self.func = zoneplate
#
#     def render():
#         plane = ne.evaluate("...")
#         return ...
#
# func(**params)
#
#
# def zoneplate(..., **kwargs):
#
# zoneplate(example=1):
#
#
# class Ellipsoid(Shape):
#     a, b = 1
#
# class Sphere(FuncOfR):
#     func:
#
# class Fresnel(Zoneplate):
#     distance, wavelength=1,
#
#
# class Zoneplate(Shape):distance
#
#
#
# shapes=[
#     { name, func, params={} }
# ]
#
# class Compound(Shape):
#     operation_type: [
#     operands: [name1, name2, name3]
#     name=(A+B)
#
#     (A+B)*C