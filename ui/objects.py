import types
from collections import OrderedDict
from dataclasses import dataclass, asdict
from enum import Enum
from inspect import signature
from typing import TypedDict, NamedTuple, Tuple

import numpy as np
import numexpr as ne
import hallucinator as hl
import tkinter as tk
import math

from ui import controls
from ui.util import build_dataclass, get_param_info_func


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


@dataclass
class SceneSettings:
    # Don't end lines with commas
    # TODO dictionaries for heterogeneous styles and densities
    autorender: bool = True
    camera_position: Tuple[float, float, float] = (0, 0, 0)
    #camera_rotation: Tuple[float, float, float] = (0, 0, 0)
    densities: Tuple[int, int] = (10, 10)
    projection_type: hl.Projections = hl.Projections.WEAK
    styles: hl.Styles = hl.Styles.UNIFORM
    x_range: Tuple[int, int] = (-5, 5)
    y_range: Tuple[int, int] = (-5, 5)
    resolution: int = 100


# NamedTuple not mutable
# TypedDict no defaults
# SimpleNamespace no signature
# @dataclass is the way!!!
@dataclass
class ViewSettings:
    style: ColorStyle = ColorStyle.GRAYSCALE
    plot_type: PlotStyle = PlotStyle.CONTOUR
    value_range: Tuple[float, float] = (-1, 1)
    resolution: int = 500
    # example_complex: complex = 1
    render_all: bool = True
    autorender: bool = True


class ComputedObject(NamedTuple):
    name: str
    func: types.FunctionType
    params: dataclass

    @classmethod
    def new(cls, name, func):
        param_defaults, param_types = get_param_info_func(func)
        # param_defaults.pop("view_settings")
        # param_types.pop("view_settings")    # FIXME this architecture is wrong...
        DataClass = build_dataclass(name, param_defaults, param_types)
        return ComputedObject(name=name, func=func, params=DataClass())

    def apply(self):
        return self.func(**asdict(self.params))


# TODO
class DerivedObject:
    name: str
    operation: Enum
    operands: list


def zone_plate(view_settings: ViewSettings, x: float = 0, y: float = 0):
    center = [x, y]
    xy = hl.xy_plane(value_range=view_settings.value_range, resolution=view_settings.resolution)
    x2y2 = ne.evaluate("sum(((xy-center)*10)**2, axis=2)")
    return hl.contour_image(x2y2, **asdict(view_settings))


def pinch_zone(view_settings: ViewSettings, x: float = 0, y: float = 0):
    center = [x, y]
    xy = hl.xy_plane(value_range=view_settings.value_range, resolution=view_settings.resolution)
    x2y2 = ne.evaluate("((xy-center)*10)**2")
    c = hl.as_complex(x2y2)
    pinch = ne.evaluate("c.real-c.imag")
    return hl.contour_image(pinch, **asdict(view_settings))


def spiral(
        location: Tuple[int, int, int] = (0, 0, 20),
        coil_density: float = 1,
        radius: float = 1,
        turns: float = 5,
        rotate_x: float = math.pi / 4):

    return hl.path_3(path_func=hl.gen_spiral(coil_density, radius),
                     p_range=(0, turns),
                     path_length=10 * math.pi).rotate(theta=rotate_x,
                                                      axis=(1, 0, 0),
                                                      p=location).translate(location)


def surface(amplitude: float = 1, frequency: float = 1,
            direction: float = math.pi,
            phase: float = math.pi,
            rotate_x: float = 0,
            rotate_y: float = 0,
            rotate_z: float = 0,
            x: int = 0,
            y: int = 0,
            z: int = 40):
    surface_obj = hl.ParaObject3(hl.gen_plane_wave(amplitude, frequency, hl.unit_vector(direction), phase),
                                 region_type='2d',
                                 region_params={'surface_range': ((-5, 5), (-5, 5))},
                                 species='surface')
    surface_obj = surface_obj.rotate(theta=rotate_x, axis=(1, 0, 0))
    surface_obj = surface_obj.rotate(theta=rotate_y, axis=(0, 1, 0))
    surface_obj = surface_obj.rotate(theta=rotate_z, axis=(0, 0, 1))
    surface_obj = surface_obj.translate((x, y, z))
    return surface_obj


available_objects = {
    # "Zone plate": zone_plate,
    # "Pinch zone": pinch_zone,
    "Surface": surface,
    #"Spiral": spiral,
}

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
