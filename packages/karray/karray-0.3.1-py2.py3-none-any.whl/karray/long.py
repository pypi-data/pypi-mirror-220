import numpy as np
try:
    import pandas as pd
    # pd.DatetimeIndex for Long.index
    # Also for Long.to_pandas()
    pandas_enabled = True
except:
    pandas_enabled = False

from html import escape
from collections import Counter
from typing import List, Dict, Tuple, Union
from .setting import settings
from .utils import _test_type_and_update, css, _format_bytes


class Long:
    def __init__(self, index:Dict[str, Union[np.ndarray, List[str], List[int], List[float]]], value:Union[np.ndarray,List[float],List[int],List[bool], bool, int, float]) -> None:
        """
        A class for working with long-format data, which consists of one or more dimensions and their corresponding coordinates, along with the values associated with each combination of coordinates across the dimensions.

        Args:
            index (dict): A dictionary of dimension names and corresponding numpy arrays of coordinates.
            value (np.ndarray): A numpy array of values associated with each combination of coordinates across the dimensions.

        Attributes:
            order (list): The order of the dimensions in the data.
            rows_display (int): The number of rows to display in the HTML representation of the Long object.
            decimals_display (int): The number of decimal places to display in the HTML representation of the Long object.
            oneshot_display (bool): Whether to display only the first set of rows in the HTML representation of the Long object.
            keep_zeros (bool): Whether to keep rows with zero values in the Long object.
            sort_coords (bool): Whether to sort the coordinates in the Long object.
            feather_with (str): The format to use when writing the data to a binary Feather file.
            fill_missing (float): The value to use for missing data when reducing the data along a dimension.

        Example:

            .. code-block:: python
        
                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6]), "z": np.array([7, 8, 9])}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)

        Methods:

            value(self) -> np.ndarray:
                Returns the value array of the Long object.

            index(self):
                returns the index of an item

            dims(self) -> List[str]:
                Returns a list of the dimensions in the Long object.

            size(self) -> int:
                Returns the number of elements in the Long object.

            items(self) -> List[Tuple[str|int, np.ndarray]]:
                returns an iterator that yields the index and value attributes of the Long object as key-value pairs.

            ndim(self) -> int:
                Returns the number of dimensions in the Long object.

            rename(self, **kwargs) -> Long:
                Renames the dimensions in the Long object based on the given keyword arguments.

            drop(self, *args) -> Long:
                Drops the specified dimensions from the Long object.

            reduce(self, dim: str, aggfunc: Callable = np.add.reduce) -> Long:
                Reduces the Long object along the specified dimension using the given aggregation function.

            insert(self, **kwargs):
                Returns a new Long object with the new dimensions and values.
        """
        # Assertion with value
        assert isinstance(value, (np.ndarray, list, float, int, bool))
        if isinstance(value, np.ndarray):
            assert issubclass(value.dtype.type, (np.bool_, np.int16, np.int32, np.int64, np.float16, np.float32, np.float64, np.float128)), "dtype suppoerted for value attribute: np.bool_, np.int16, np.int32, np.int64, np.float16, np.float32, np.float64, np.float128"
            if value.ndim == 0:
                value = value.reshape((value.size,))
        elif isinstance(value, (float, int, bool)):
            value = np.array([value])
        elif isinstance(value, list):
            if value:
                if isinstance(value[0], str):
                    raise NotImplementedError("Long object does not support string values for value attribute")
                elif isinstance(value[0], (int, float, bool)):
                    value = np.array(value)
                elif issubclass(value[0].dtype.type, (np.bool_, np.int16, np.int32, np.int64, np.float16, np.float32, np.float64, np.float128)):  # Assuming numpy
                    value = np.array(value)
            else: # Empty list
                value = np.array(value, dtype=None)

        assert value.ndim == 1
        # Assertion with index
        assert isinstance(index, dict)
        if pandas_enabled:
            assert all([isinstance(index[dim], (np.ndarray, list, pd.DatetimeIndex)) for dim in index])
        else:
            assert all([isinstance(index[dim], (np.ndarray, list)) for dim in index])
        dims = list(index)
        for dim in dims:
            index[dim] = _test_type_and_update(index[dim])

        assert all([index[dim].ndim == 1 for dim in index])
        assert all([index[dim].size == value.size for dim in index])
        assert 'value' not in index, "'value' can not be a dimension name as it is reserved"
        assert all([isinstance(dim, str) for dim in index])

        self._value = value
        self._index = index
        self._dims = list(self._index)

        self.rows_display = settings.rows_display
        self.decimals_display = settings.decimals_display
        self.oneshot_display = settings.oneshot_display
        self.long_nbytes = _format_bytes(sum([self._index[dim].nbytes for dim in self._index] + [self._value.nbytes]))

    def __repr__(self) -> str:
        return f'''Long
    Object size: {self.long_nbytes}
    Dimensions: {self.dims}
    Rows: {self._value.size}'''

    def _repr_html_(self) -> str:
        dims = self.dims
        items = self._value.size

        if items > self.rows_display:
            short = False
            if self.oneshot_display:
                rows = self.rows_display
            else:
                rows = int(self.rows_display/2)
        else:
            short = True
            rows = items

        columns = dims + ['value']
        html = [f"{css}"]
        html += ['<h3>[Long]</h3>',
                '<table>',
                f'<tr><th>Long object size</th><td>{self.long_nbytes}</td></tr>',
                "<!-- DENSE -->",
                f'<tr><th>Dimensions</th><td>{dims}</td></tr>',
                '<!-- SHAPE -->',
                f'<tr><th>Rows</th><td>{items}</td></tr>',
                '</table>']
        html += ["<!-- COORDS -->"]
        html += [f"<details>"]
        html += [f'<table><summary><div class="tooltip"> Show data <small>[default: 16 rows, 2 decimals]</small>']
        html += [f'<!-- A --><span class="tooltiptext tooltip-top">To change default values:<br> obj.rows_display = Int val<br>obj.decimals_display = Int val<br>obj.oneshot_display = False<!-- Z -->']
        html += ['</span></div></summary><tr><th>']
        html += [f"<th>{j}" for j in columns]
   
        for i in range(rows):
            html.append(f"<tr><th><b>{i}</b>")
            for j,v in self.items():
                val = v[i]
                html.append("<td>")
                html.append(escape(f"{val:.{self.decimals_display}f}" if issubclass(v.dtype.type, float) else f"{val}"))

        if not self.oneshot_display:
            if not short:
                html.append("<tr><th>")
                for _ in range(len(dims)+1):
                    html.append("<td>...")
                for i in range(items-rows,items,1):
                    html.append(f"<tr><th><b>{i}</b>")
                    for j,v in self.items():
                        val = v[i]
                        html.append("<td>")
                        html.append(escape(f"{val:.{self.decimals_display}f}" if issubclass(v.dtype.type, float) else f"{val}"))
        html.append("</table></details>")
        return "".join(html)

    @property
    def index(self):
        """
        returns the index as dictionary

        Returns:
            Dict: dict-item that represents the index of the long object.

        Example:

            .. code-block:: python

                >>> long = ka.Long({'one':np.array(['2022-11-25'])}, [4.0])
                >>> long.index
                {'one': np.array(['2022-11-25'])}

    """
        assert set(self.dims) == set(self._index.keys()), "dims names must match with index names" 
        return {dim:self._index[dim] for dim in self.dims}

    @property
    def value(self):
        """
        returns a numpy array of floats that represents the value of the long object.

        Returns: 
            copy of the _value numpy array, which represents the data stored in the object.
        
        Example:

            .. code-block:: python

                >>> long = ka.Long({'one':np.array(['2022-11-25'])}, [4.0])
                >>> long.value
                np.array([4.0])
        
        """
        return self._value.copy()

    @property
    def dims(self):
        """
        Returns a list of the dimensions in the Long object.

        Returns:
            List[str]: A list of the dimensions in the Long object.

        Example:

            .. code-block:: python

                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6]), "z": np.array([7, 8, 9])}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)
                >>> long.dims()
                ['x', 'y', 'z']

        """
        return self._dims[:]

    @property
    def size(self):
        """
        Returns the number of elements of the value attribute in the Long object.

        Returns:
            int: The number of elements of the value attribute in the Long object.

        Example:

            .. code-block:: python

                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6]))}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)
                >>> long.size()
                3
        """
        return self.value.size

    @property
    def ndim(self):
        """
        Returns the number of dimensions in the Long object.

        Returns:
            int: The number of dimensions in the Long object.

        Example:

            .. code-block:: python

                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6]), "z": np.array([7, 8, 9])}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)
                >>> long.ndim()
                3

        """
        return len(self.index)

    def insert(self, **kwargs):
        """
        Insert a new dimensions in different ways. first the new dimension must be provided. See details below and example.
        
        Args: 
            **kwargs (dict): A dictionary of dimension names and their corresponding options. Option 1. a scalar or string that represents the unique element of the new dimension, Option 2. A mapping dictionary to another existing dimension, or a list with a mapping of the existing dimension to the new.
        Returns: 
            Long: A new Long object with the updated dimensions and values.

        Example:

            .. code-block:: python

                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6])}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)

                >>> long.insert(id=1).items()
                [('id', np.array([1, 1, 1])), ("x", np.array([1, 2, 3])), ("y", np.array([4, 5, 6])), ('value', np.array([0.1, 0.2, 0.3]))]


                >>> long.insert(w={'x':{1:'n', 2:'m', 3:'q'}}).items()
                [('w', np.array(['n', 'm', 'q'])), ("x", np.array([1, 2, 3])), ("y", np.array([4, 5, 6])), ('value', np.array([0.1, 0.2, 0.3]))]

                
                >>> long.insert(t={'y':[[4,5,6], ['a','b','c']]}).items()
                [('t', np.array(['a', 'b', 'c'])), ("x", np.array([1, 2, 3])), ("y", np.array([4, 5, 6])), ('value', np.array([0.1, 0.2, 0.3]))]

        """
        assert all([dim not in self.dims for dim in kwargs])
        assert all([isinstance(kwargs[dim], (str, int, dict, np.dtype, type)) for dim in kwargs])
        for dim in kwargs:
            if isinstance(kwargs[dim], dict):
                value = kwargs[dim]
                assert len(value) == 1
                existing_dim = next(iter(value))
                assert isinstance(existing_dim, (str,tuple))
                if isinstance(existing_dim, tuple):
                    assert all([dim in self.dims for dim in existing_dim])
                else:
                    assert existing_dim in self.dims
                assert isinstance(value[existing_dim], (dict, list))
                if isinstance(existing_dim, str):
                    if isinstance(value[existing_dim], dict):
                        old_dim_items = list(value[existing_dim])
                        old_dim_items_set = set(old_dim_items)
                    elif isinstance(value[existing_dim], list):
                        kwargs[dim][existing_dim][0] = _test_type_and_update(value[existing_dim][0])
                        kwargs[dim][existing_dim][1] = _test_type_and_update(kwargs[dim][existing_dim][1])
                        old_dim_items = kwargs[dim][existing_dim][0]
                        old_dim_items_set = set(old_dim_items)
                    assert set(np.unique(self.index[existing_dim])).issubset(old_dim_items_set)
                    assert len(old_dim_items) == len(old_dim_items_set) # mapping has unique keys
                elif isinstance(existing_dim, tuple):
                    if isinstance(value[existing_dim], dict):
                        raise NotImplementedError("TODO")
                    elif isinstance(value[existing_dim], list):
                        kwargs[dim][existing_dim][1] = _test_type_and_update(kwargs[dim][existing_dim][1])

        index = {}
        for new_dim in kwargs:
            value = kwargs[new_dim]
            if isinstance(value, (np.dtype, type)):
                assert self._value.size == 0
                idxarray = np.empty(self.size, dtype=value)
            elif isinstance(value, str):
                idxarray = np.empty(self.size, dtype=np.object_)
                idxarray[:] = value
            elif isinstance(value, int):
                idxarray = np.empty(self.size, dtype=np.int64)
                idxarray[:] = value
            elif isinstance(value, dict):
                existing_dim = next(iter(value))
                if isinstance(existing_dim, str):
                    if isinstance(value[existing_dim], dict):
                        mapping_dict = value[existing_dim]
                        existing_dim_items = self.index[existing_dim]
                        k = np.array(list(mapping_dict)) # This must be unique
                        v = np.array(list(mapping_dict.values())) # This not necessary unique
                    elif isinstance(value[existing_dim], list):
                        assert isinstance(value[existing_dim][0],np.ndarray)
                        assert isinstance(value[existing_dim][1],np.ndarray)
                        k = value[existing_dim][0]
                        v = value[existing_dim][1]
                        existing_dim_items = self.index[existing_dim]
                    else:
                        raise Exception(f"type {type(value[existing_dim])} not implemented.")

                    idxarray = np.array(v)[np.argsort(k)[np.searchsorted(k, existing_dim_items, sorter=np.argsort(k))]]
                elif isinstance(existing_dim, tuple):
                    if isinstance(value[existing_dim], dict):
                        raise NotImplementedError("TODO")
                    elif isinstance(value[existing_dim], list):
                        assert isinstance(value[existing_dim][1],np.ndarray)
                        coords = value[existing_dim][0]
                        new_dim_elements = value[existing_dim][1]
                        collect_index = []
                        for dim in existing_dim:
                            a = np.argsort(coords[dim])[np.searchsorted(coords[dim], self.index[dim], sorter=np.argsort(coords[dim]))]
                            collect_index.append(a)
                        index_index = np.vstack(collect_index)
                        shape = [coords[dim].size for dim in coords]
                        indexes = np.ravel_multi_index(index_index, shape)
                        # capacity = int(np.prod(shape))
                        # unique_combination = np.unravel_index(np.arange(capacity), shape)
                        # unique = np.vstack(unique_combination)
                        # mask = np.argwhere(unique == index_index)
                        # mask = np.searchsorted(unique, index_index)
                        idxarray = new_dim_elements[indexes]
                    else:
                        raise Exception(f"type {type(value[existing_dim])} not implemented.")
            index[new_dim] = idxarray

        for dim in self.index:
            index[dim] = self.index[dim]

        return Long(index=index, value=self.value)
    
    def rename(self, **kwargs):
        """
        Renames the dimensions in the Long object based on the given keyword arguments.

        Args:
            **kwargs (dict): A dictionary of dimension names and their new names.

        Returns:
            Long: A new Long object with the renamed dimensions.

        Example:

            .. code-block:: python

                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6]), "z": np.array([7, 8, 9])}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)
                >>> long.rename(x="new_x", y="new_y", z="new_z").dims()
                ['new_x', 'new_y', 'new_z']

        """
        assert all([odim in self.dims for odim in kwargs])
        assert all([ndim not in self.dims for ndim in kwargs.values()])
        index = {}
        for dim in self.dims:
            if dim in kwargs:
                index[kwargs[dim]] = self._index[dim]
            else:
                index[dim] = self._index[dim]
        return Long(index=index, value=self._value)

    def drop(self, dims:Union[str,List[str]]):
        """
        Drops the specified dimensions from the Long object.

        Args:
            dims (Union[str,List[str]]): The names of the dimensions to drop.

        Returns:
            Long: A new Long object with the specified dimensions dropped.

        Example:

            .. code-block:: python

                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6]), "z": np.array([7, 8, 9])}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)
                >>> long.drop("z").dims()
                ['x', 'y']

        """
        assert isinstance(dims, (str, list))
        index = {}
        if isinstance(dims, str):
            assert dims in self.dims
            dims = [dims]
        elif isinstance(dims, list):
            assert all([dim in self.dims for dim in dims])
        for dim in self.dims:
            if dim not in dims:
                index[dim] = self._index[dim]
        item_tuples = list(zip(*index.values()))
        if len(set(item_tuples)) == len(item_tuples):
            flag = True
        else:
            flag=False
            counts = Counter(item_tuples)
            most_common = counts.most_common(1)[0][0]
            first = item_tuples.index(most_common,0)
            second  = item_tuples.index(most_common,first+1)
            display_str = f"e.g.:\n  {tuple(index)} value\n{first} {item_tuples[first]} {self._value[first]}\n{second} {item_tuples[second]} {self._value[second]}"
        assert flag, f"Index items per row must be unique. By removing {dims} leads the existence of repeated indexes \n{display_str}\nIntead, you can use obj.reduce('{dims[0]}')\nWith an aggfunc: sum() by default"
        return Long(index=index, value=self._value)
        
    def items(self):
        """
        Returns a list of the dimensions and corresponding numpy arrays and the value with its numpy array as part of the Long object.

        Returns:
            List[Tuple[str, np.ndarray]]: A list of the dimensions and corresponding numpy arrays and also the value in the Long object.

        Example:

            .. code-block:: python

                >>> index = {"x": np.array([1, 2, 3]), "y": np.array([4, 5, 6]), "z": np.array([7, 8, 9])}
                >>> value = np.array([0.1, 0.2, 0.3])
                >>> long = Long(index, value)
                >>> long.items()
                [('x', array([1, 2, 3])), ('y', array([4, 5, 6])), ('z', array([7, 8, 9])), ('value', np.array([0.1, 0.2, 0.3]))]
        """
        dc = dict(**self.index)
        dc.update(dict(value=self._value))
        for k,v in dc.items():
            yield (k,v)

    def __getitem__(self, item):
        """
        Gets values from the Long object by accessing its index.

        Args:
            item (Integer | Numpy Array | Slice | String | Tuple): indexes the long object
        
        Returns: Long object with the specified indices and values.
        
        Example:

            .. code-block:: python

                >>> long = ka.Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64')}, [4.0, 5.0, 6.0])
                >>> long['one', np.array(['2022-11-23'], dtype='datetime64')]
                ka.Long({'one': np.array(['2022-11-23'], dtype='datetime64')},[6.0])
                

                >>> long = ka.Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'])}, [4.0, 5.0, 6.0])
                >>> long['one', np.array(['2022-11-23'])]
                ka.Long({'one': np.array(['2022-11-23'])},[6.0])
                

                >>> long = ka.Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'])}, [4.0, 5.0, 6.0])
                >>> long['one', np.array(['2022-11-23'])]
                ka.Long({'one': np.array(['2022-11-23'])},[6.0])
                

                >>> long = ka.Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'])}, [4.0, 5.0, 6.0])
                >>> long['one', np.array([('2022-11-23')])]
                ka.Long({'one': np.array([('2022-11-23')])},[6.0])
                

                >>> value = np.array([1, 2, 3])
                >>> long = ka.Long({'one': value}, [4.0, 5.0, 6.0])
                >>> long['one', (value[2:3])]
                ka.Long({'one':[3]},[6.0])

        """
        assert isinstance(item, (str, int, list, np.ndarray, slice, tuple))
        if isinstance(item, int):
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        elif isinstance(item, list):
            item = np.array(item, dtype=np.int64)
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        elif isinstance(item, np.ndarray):
            assert issubclass(item.dtype.type, np.int64) or issubclass(item.dtype.type, np.bool_)
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        elif isinstance(item, slice):
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        elif isinstance(item, str):
            assert item in self.dims
            return self._index[item]
        elif isinstance(item, tuple):
            assert len(item) == 2
            if isinstance(item[0], str):
                dim = item[0]
                condition = item[1]
                assert dim in self.dims
                assert isinstance(condition, (list, np.ndarray, slice))
                index_items_on_dim = self._index[dim]
                # Go over the elements of the numpy array
                if isinstance(condition, (list,np.ndarray)):
                    mask = np.isin(index_items_on_dim, condition)
                    return Long(index={dim_:self._index[dim_][mask] for dim_ in self.dims}, value=self._value[mask])
                # only works if elements of the numpy array are integers
                elif isinstance(condition, slice):
                    assert issubclass(index_items_on_dim.dtype.type, np.int64)
                    start = condition.start or int(np.min(index_items_on_dim))
                    step = condition.step or 1
                    stop = condition.stop or int(np.max(index_items_on_dim) + step)
                    arange_condition = np.arange(start,stop,step)
                    mask = np.isin(index_items_on_dim, arange_condition)
                    return Long(index={dim_:self._index[dim_][mask] for dim_ in self.dims}, value=self._value[mask])
            # Reorder dims
            elif isinstance(item[0], list):
                reorder = item[0]
                assert set(self.dims) == set(reorder)
                assert isinstance(item[1], slice)
                condition = item[1]
                start = condition.start or 0
                stop = condition.stop or self._value.size
                step = condition.step or 1
                arange_condition = np.arange(start,stop,step)
                return Long(index={dim_:self._index[dim_][arange_condition] for dim_ in reorder}, value=self._value[arange_condition])
            # TODO: Implement slice over datetime

    def __eq__(self, __o: object):
        """
        This method implements the equality operator (`==`) for the `Long` class.

        Args:
            __o (object): Input object to be compared with the `self` object.

        Returns:
            bool: Returns True if the values are equal, False otherwise.

        Raises:
            Exception: If the type of `__o` is not supported, an exception is raised.

        Example:

            .. code-block:: python

                >>> A = ka.Long({'one':['2022-11-25', '2022-11-24','2022-11-23']}, [4.0, 5.0, 6.0])
                >>> B = ka.Long({'one':['2022-11-25', '2022-11-24','2022-11-23']}, [4.0, 5.0, 6.0])
                >>> A == B
                True

        """
        if isinstance(__o, Long):
            dims_equal = tuple(self.dims) == tuple(__o.dims)
            if not dims_equal:
                return False
            value_equal = np.array_equal(self._value,__o._value)
            if not value_equal:
                return False
            return all(np.array_equal(self._index[dim],__o._index[dim]) for dim in self.dims)
        else:
            if np.isnan(__o):
                return np.isnan(self._value)
            elif np.isinf(__o):
                return np.isinf(self._value)
            elif isinstance(__o, (int,float)):
                return self._value == __o
            elif isinstance(__o, np.generic):
                raise Exception("np.ndarray not supported yet")
            else:
                raise Exception(f"{type(__o)} not supported yet")

    def __ne__(self, __o: object):
        """
        Compares if the values of two Long objects are not equal.

        Args:
            __o (object): Input object to be compared with the `self` object.
        
        Returns:
            bool: Returns True if the values are not equal, False otherwise.
        
        Raises:
            Exception: If the input object is of a type that is not supported, an exception is raised.
        
        Example:

            .. code-block:: python

                >>> A = ka.Long({'one':['2022-11-25', '2022-11-24','2022-11-23']}, [4.0, 5.0, 6.0])
                >>> B = ka.Long({'one':['2022-11-25', '2022-11-24','2022-11-23']}, [4.0, 5.0, 6.0])
                >>> A != B
                False

        """
        if isinstance(__o, Long):
            dims_equal = tuple(self.dims) == tuple(__o.dims)
            if not dims_equal:
                return True
            value_equal = np.array_equal(self._value,__o._value)
            if not value_equal:
                return True
            return not all(np.array_equal(self._index[dim],__o._index[dim]) for dim in self.dims)
        else:
            if np.isnan(__o):
                return ~np.isnan(self._value)
            elif np.isinf(__o):
                return ~np.isinf(self._value)
            elif isinstance(__o, (int,float)):
                return self._value != __o
            elif isinstance(__o, np.generic):
                raise Exception("np.ndarray not supported yet")
            else:
                raise Exception(f"{type(__o)} not supported yet")
            
    def __lt__(self, __o: object):
        """
        Check whether the first operand is strictly less than the second operand element-wise.

        Args:
            __o (object): Object to be compared with `self`.

        Returns:
            Bool: Boolean result of the operation.
        
        Raises:
            Exception)

        """
        if isinstance(__o, (int,float)):
            return np.less(self._value, __o)
        elif isinstance(__o, np.ndarray):
            return np.less(self._value, __o)
        elif isinstance(__o, Long):
            return np.less(self._value, __o._value)
        else:
            raise Exception(f"Operation not supported on {type(__o)}")

    def __le__(self, __o: object):
        """
        Check whether the first operand is less than or equal to the second operand element-wise.

        Args:
            __o (object): Object to be compared with `self`.

        Returns:
            Bool: Boolean result of the operation.
        
        Raises:
            Exception)

        """
        if isinstance(__o, (int,float)):
            return np.less_equal(self._value, __o)
        elif isinstance(__o, np.ndarray):
            return np.less_equal(self._value, __o)
        elif isinstance(__o, Long):
            return np.less_equal(self._value, __o._value)
        else:
            raise Exception(f"Operation not supported on {type(__o)}")

    
    def __gt__(self, __o: object):
        """
        Check whether the first operand is strictly greater than the second operand element-wise.

        Args:
            __o (object): Object to be compared with `self`.

        Returns:
            Bool: Boolean result of the operation.
        
        Raises:
            Exception

        """
        if isinstance(__o, (int,float)):
            return np.greater(self._value, __o)
        elif isinstance(__o, np.ndarray):
            return np.greater(self._value, __o)
        elif isinstance(__o, Long):
            return np.greater(self._value, __o._value)
        else:
            raise Exception(f"Operation not supported on {type(__o)}")

    
    def __ge__(self, __o: object):
        """
        Check whether the first operand is greater than or equal to the second operand element-wise.

        Args:
            __o (object): Object to be compared with `self`.

        Returns:
            Bool: Boolean result of the operation.
        
        Raises:
            Exception

        """
        if isinstance(__o, (int,float)):
            return np.greater_equal(self._value, __o)
        elif isinstance(__o, np.ndarray):
            return np.greater_equal(self._value, __o)
        elif isinstance(__o, Long):
            return np.greater_equal(self._value, __o._value)
        else:
            raise Exception(f"Operation not supported on {type(__o)}")


    def to_pandas(self):
        if pandas_enabled:
            pass
        else:
            raise Exception("pandas not installed. Install with `pip install pandas`")
        data = {dim:self._index[dim] for dim in self.dims}
        data['value'] = self._value
        return pd.DataFrame(data=data)