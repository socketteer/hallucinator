import collections
import itertools
from functools import lru_cache

import numpy as np
import numexpr as ne
from pathos.multiprocessing import ProcessingPool


################################################################################
# Numpy
################################################################################

# Normalize an array, defaults from [min, max] to [0, 1]
# copy=True will not affect the original array
def normalize_array(arr, from_range=None, to_range=None, use_ne=True):
    if not from_range:
        from_range = [arr.min(), arr.max()]

    # from [a,b] to [c,d]
    a = from_range[0] if from_range else arr.min()
    b = from_range[1] if from_range else arr.max()
    c = to_range[0] if to_range else 0
    d = to_range[1] if to_range else 1

    # Subtract a, divide by len[a,b], multiply by len[c,d], add c
    if use_ne:
        return ne.evaluate("(arr-a) * (d-c)/(b-a) + c")
    else:
        arr -= a
        arr *= (d-c)/(b-a)  # Multiplication faster than division
        if c != 0:
            arr += c
        return arr


# Reinterpret as complex numbers and then ditch the extra dimension [1000,1000,2]->[1000,1000]
def as_complex(xy):
    if xy.dtype == np.float32:
        new_dtype = np.complex64
    elif xy.dtype == np.float64:
        new_dtype = np.complex128
    else:
        raise ValueError(f"Unsupported dtype {xy.dtype}")
    return xy.view(dtype=new_dtype)[..., 0]


# Reinterpret a complex array as x,y coordinates [1000,1000] -> [1000,1000,2]
# Requires a C-continuous array...
def as_xy(complex_arr):
    if complex_arr.dtype == np.complex64:
        new_dtype = np.float32
    elif complex_arr.dtype == np.complex128:
        new_dtype = np.float64
    else:
        raise ValueError(f"Unsupported dtype {complex_arr.dtype}")
    xy = complex_arr.view(dtype=new_dtype)
    return xy.reshape(complex_arr.shape + (2,))


# Returns an array of shape (resolution[0], resolution[1]) of complex numbers
def complex_plane(value_range=(-1, 1), resolution=1000, **kwargs):
    return as_complex(xy_plane(value_range, resolution))


def xy_plane(value_range=(-1, 1), resolution=(1000, 1000), grid=True, **kwargs):
    """
    :param value_range: Float 2tuple or 2d array of x range, y range
    :param resolution: Scalar or 2tuple. The number of points to sample from range in the x and y directions
        defaults to image_size
    :return: xy plane with shape (resolution_x, resolution_y, 2)
    """
    return _xy_plane(tuplify(value_range), tuplify(resolution), grid)


# Cache the last N function call results.
# If the function is called again with the same arguments, the cached result is used
# Can only be used with immutable, hashable arguments
@lru_cache(maxsize=16)
def _xy_plane(value_range=(-1, 1), resolution=(1000, 1000), grid=True):
    resolution_x = resolution[0] if isinstance(resolution, collections.abc.Sequence) else resolution
    resolution_y = resolution[1] if isinstance(resolution, collections.abc.Sequence) else resolution
    value_range_x = value_range[0] if isinstance(value_range[0], collections.abc.Sequence) else value_range
    value_range_y = value_range[1] if isinstance(value_range[0], collections.abc.Sequence) else value_range

    x_axis = np.linspace(start=value_range_x[0], stop=value_range_x[1], num=int(resolution_x))
    y_axis = np.linspace(start=value_range_y[0], stop=value_range_y[1], num=int(resolution_y))
    # Perturb if not a grid
    if not grid:
        x_step = (x_axis[1] - x_axis[0])
        x_axis += np.random.uniform(low=-x_step, high=x_step, size=x_axis.shape)
        y_step = (x_axis[1] - x_axis[0])
        y_axis += np.random.uniform(low=-y_step, high=y_step, size=y_axis.shape)

    # meshgrid returns an array of x coords and an array of y coords (shape(1000,1000), shape(1000,1000))
    meshgrid = np.meshgrid(x_axis, y_axis)
    # stacking gives an array where the last axis is the (x,y) pair in X cross Y.
    xy = np.stack(meshgrid, axis=2)
    # shape: (1000, 1000, 2)
    return xy


def sample_function(function,
                    value_range=(-1, 1),
                    resolution=(1000, 1000),
                    grid=True,
                    parallel=True,
                    **params):
    """
    Sample a function over an xy plane with the given value range and resolution.
    Function is called with ((x,y), **params)
    Returns an array of shape (resolution_x, resolution_y, *function_shape),
        e.g. (1000,1000,3) if f(p)=[a,b,c]
        e.g. (1000,1000,3,3) if f(p).shape=(3,3)
    """
    # TODO make over any number of dimensions?

    xy = xy_plane(value_range, resolution, grid=grid)
    if parallel:
        # Flatten into array of 2d points [(x,y), ...]
        points = xy.reshape(-1, xy.shape[-1])
        with ProcessingPool() as pool:
            values = pool.map(lambda p: function(p, **params), points)
        sampled = np.resize(values, xy.shape[:-1])  # TODO Doesn't work for non-scalar functions
    else:
        sampled = np.apply_along_axis(lambda p: function(p, **params), 2, xy)

    # returns shape: (resolution_x, resolution_y, *function_shape)
    return sampled


################################################################################
# Data structures
################################################################################


# Break a list into parts of a given size, allowing the last element to be shorter
def grouper(iterable, size):
    # "grouper(3, 'ABCDEFG') --> [ABC, DEF, G]"
    it = iter(iterable)
    while True:
        group = tuple(itertools.islice(it, None, size))
        if not group:
            break
        yield group


# Add an item between each element of a list
# intersperse([1, 2, 3], '-') = [1, '-', 2, '-', 3]
def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


# Apply a function recursively to all elements in nested lists. Doesn't work for numpy arrays...? :'(
def recursive_map(func, li, on_elements=True, on_list=False):
    if isinstance(li, collections.abc.Sequence) or (isinstance(li, np.ndarray)):
        # Self containing lists... Just give up. No map is worth that recursion.
        if not li in li:
            li = list(map(lambda x: recursive_map(func, x, on_elements, on_list), li))
        return func(li) if on_list else li
    else:
        return func(li) if on_elements else li


# Turn nested lists or numpy arrays into tuples.
# Useful for preparing lists for printing or making them immutable for caching
def tuplify(l):
    return recursive_map(tuple, l, on_elements=False, on_list=True)


# Tuplify and round to n digits. Useful for display
def tupliround(li, num_digits=3):
    return tuplify(recursive_map(lambda x: round(x, num_digits), li))


# Given a dictionary which contains lists, find the longest length L
# Unroll all lists with len(L), creating a list of len(L) of dictionaries with the same
# key:value pairs, but a single value for each key which contained a list of len(L).
# Add a key __index to each dictionary corresponding to its place in the list
# This allows you to create param dicts which interpolate over multiple keys at the same time
#
# E.g. unroll_dict({
#   param1 = True,
#   param2 = [a, b, c],
#   param3 = [d, e, f],
#   param4 = [g, h]
# }) == [
#    {param1=True, param2=a, param3=d, param4=[g, h]}
#    {param1=True, param2=b, param3=e, param4=[g, h]}
#    {param1=True, param2=c, param3=f, param4=[g, h]}
#  ]
def unroll_dict(dict_of_lists):
    # Find longest list in dict
    longest_len = 0
    for key, value in dict_of_lists.items():
        try:
            longest_len = max(longest_len, len(value))
        except Exception:
            pass

    # Make a list of dicts, unrolling the longest key lists
    list_of_dicts = []
    for i in range(longest_len):
        d = {}
        for key, value in dict_of_lists.items():
            try:
                if len(value) == longest_len:
                    d[key] = value[i]
                    continue
            except Exception:
                pass
            d[key] = value
        d["__index"] = i
        list_of_dicts.append(d)

    return list_of_dicts


################################################################################
# Tests
################################################################################


def test_normalize_array():
    a = np.random.rand(100, 100)# * 100 - 400
    a = normalize_array(a)
    assert a.max() == 1
    assert a.min() == 0
    print(a.mean())

    a = np.random.rand(100, 100, 100)
    a = normalize_array(a, from_range=(-1, 1))
    assert a.min() > 0.5
    print(a.mean())

    a = np.random.rand(100, 100, 100)
    a = normalize_array(a, from_range=(0, 1), to_range=(0, 255))
    assert 0 <= a.min() < 1
    assert 254 < a.max() <= 255
    print(a.mean())


def test_complex_plane():
    a = complex_plane()
    print(type(a), a.dtype, a.shape)
    print(a.max(), a.min())

    a = as_xy(a)
    print(type(a), a.dtype, a.shape)
    print(a.max(), a.min())

    a = as_complex(a)
    print(type(a), a.dtype, a.shape)
    print(a.max(), a.min())



if __name__ == "__main__":
    test_normalize_array()
    test_complex_plane()
