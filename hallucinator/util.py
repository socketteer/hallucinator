import collections
from functools import lru_cache

import numpy as np
import numexpr as ne
from pathos.multiprocessing import ProcessingPool


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


# Cache the last N function call results.
# If the function is called again with the same arguments, the cached result is used
# Can only be used with immutable, hashable arguments
@lru_cache(maxsize=16)
def xy_plane(value_range=(-1, 1), resolution=(1000, 1000), grid=True):
    """
    :param value_range: Float 2tuple or 2d array of x range, y range
    :param resolution: Scalar or 2tuple. The number of points to sample from range in the x and y directions
        defaults to image_size
    :return: xy plane with shape (resolution_x, resolution_y, 2)
    """
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


if __name__ == "__main__":
    test_normalize_array()
