from typing import Any, Optional

import numpy as np

from akkits.schema.tracklet_packet.Vector3 import Vector3


def table_to_np_array(obj: Any) -> Optional[np.ndarray]:
    """Creates a NumPy array from a flatbuffer `Table` with fields: `shape`, `data`.

    `shape` should be a vector of ints. `data` should be a vector of ints or floats.

    Args:
        obj (Any): A `Table` object with methods `DataAsNumpy` and `ShapeAsNumpy`. Can be `None`.

    Returns:
        arr (Optional[np.ndarray]): The `Table` as an array.
            If input is `None`, then returns `None`.
    """
    return obj if obj is None else obj.DataAsNumpy().reshape(obj.ShapeAsNumpy())


def vec3_to_np_array(obj: Optional[Vector3], dtype=np.float32) -> Optional[np.ndarray]:
    """Creates a NumPy array from a flatbuffer `Vector3` `struct` with fields: `X`, `Y`, `Z`.

    All `X`, `Y`, `Z` should be an int or a float.

    Args:
        obj (Optional[Vector3]): A `Vector3` object. Can be `None`.
        dtype (_type_, optional): The output array data type. Defaults to `np.float32`.

    Returns:
        arr (Optional[np.ndarray]): The `Vector3` as an array.
            If input is `None`, then returns `None`.
    """
    return None if obj is None else np.array((obj.X(), obj.Y(), obj.Z()), dtype=dtype)
