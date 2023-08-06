from typing import List, Dict, Tuple, Union
import numpy as np
try:
    import pandas as pd
    pandas_enabled = True
except:
    pandas_enabled = False

def union_multi_coords(*args: List[Dict[str, np.ndarray]]) -> Dict[str, np.ndarray]:
    '''
    Return the union of multiple coordinates.

    Parameters:
        *args (list[dict[str, np.ndarray]]): List of dictionaries containing keys as dimensions and values as numpy arrays.

    Returns:
        dict[str, np.ndarray]: A dictionary containing the union of all input numpy arrays for each dimension.
    '''
    assert all([tuple(coords) == tuple(args[0]) for coords in args])
    dims = list(args[0])
    new_coords = {}
    for coords in args:
        for dim in dims:
            if dim not in new_coords:
                new_coords[dim] = coords[dim]
            else:
                if new_coords[dim].size == coords[dim].size:
                    if all(new_coords[dim] == coords[dim]):
                        continue
                    else:
                        new_coords[dim] = np.union1d(new_coords[dim], coords[dim])
                elif set(new_coords[dim]).issubset(set(coords[dim])):
                    new_coords[dim] = coords[dim]
                elif set(coords[dim]).issubset(set(new_coords[dim])):
                    continue
                else:
                    new_coords[dim] = np.union1d(new_coords[dim], coords[dim])
    return new_coords

def _test_type_and_update(item: Union[List[str], List[int], List[float], List[np.datetime64], np.ndarray]) -> np.ndarray:
    """
    Converts a list or array of values to a NumPy array of a suitable type.

    Args:
        item: A list or array of values.

    Returns: 
        A NumPy array with the same data as `item`, converted to a suitable dtype if necessary.
    """
    if len(item) == 0: #
        if isinstance(item, np.ndarray):
            return item.copy()
        else:
            return np.array([]) # it will be a float64, Maybe change to np.object_
    else:
        if isinstance(item, np.ndarray):
            if issubclass(type(item[0]), str):
                if issubclass(item.dtype.type, np.object_):
                    variable_out = item.copy()
                elif issubclass(item.dtype.type, str):
                    variable_out = item.astype('object')
                else:
                    raise Exception(f"item: {item}, type: {type(item[0])} not implemented")
            elif issubclass(item.dtype.type, np.object_):
                if issubclass(type(item[0]), int):
                    variable_out = item.astype(int)
                elif isinstance(type(item[0]), float):
                    variable_out = item.astype(float)
                else:
                    raise Exception(f"item: {item}, type: {type(item[0])} not implemented")
            elif issubclass(item.dtype.type, (np.int16, np.int32, np.int64)):
                variable_out = item.copy()
            elif issubclass(item.dtype.type, (np.float16, np.float32, np.float64, np.float128)):
                variable_out = item.copy()
            elif issubclass(item.dtype.type, np.datetime64):
                variable_out = item.copy()
            else:
                raise Exception(f"item: {item}, type: {type(item[0])} not implemented")
        elif isinstance(item, list):
            value_type = type(item[0])
            if issubclass(value_type, str):
                selected_type = 'object'
            elif issubclass(value_type, int):
                selected_type = 'int'
            elif issubclass(value_type, np.datetime64):
                selected_type = 'datetime64[ns]'
            elif issubclass(value_type, float):
                selected_type = 'float'
            else:
                raise Exception(f"item: {item}, type: {type(item[0])} not implemented")
            variable_out = np.array(item, dtype=selected_type)
        elif pandas_enabled:
            if isinstance(item, pd.DatetimeIndex):
                variable_out = item.values
            else:
                raise Exception(f"item: {item}, type: {type(item)} not implemented")
        else:
            raise Exception(f"item: {item}, type: {type(item)} not implemented")
        return variable_out

def _format_bytes(size: int):
    """
    Format bytes to human readable format.

    Thanks to: https://stackoverflow.com/a/70211279
    """
    power_labels = {40: "TB", 30: "GB", 20: "MB", 10: "KB"}
    for power, label in power_labels.items():
        if size >= 2 ** power:
            approx_size = size / 2 ** power
            return f"{approx_size:.1f} {label}"
    return f"{size} bytes"

css = '''<style>
.details {user-select: none;}
.details>summary .span.icon {width: 24px;height: 24px;transition: all 0.3s;margin-left: auto;}
.details[open].summary.span.icon{transform:rotate(180deg);}
.summary{display:flex;cursor:pointer;} 
.summary::-webkit-details-marker{display:none;}
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 165px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 4px;
  padding: 2px 0;
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  font-size: 11px;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
}
.tooltip-top {
 bottom: 90%;
 margin-left: -40px;
 }
</style>'''
