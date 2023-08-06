import numpy as np
import pytest
from karray import Long, Array
from numpy.testing import assert_array_equal



@pytest.fixture
def long_obj_with_str():
    # create an Long object for testing
    indexes = {'one':['aaa', 'bbb','ccc']}
    values = [4.0, 5.0, 6.0]
    return Long(index=indexes, value=values)

@pytest.fixture
def long_obj_with_int():
    # create an Long object for testing
    indexes = {'one': [1, 2, 3, 5]}
    values = [4.0, 5.0, 6.0, 7.0]
    return Long(index=indexes, value=values)

@pytest.fixture
def long_obj_with_dt():
    # create an Long object for testing
    indexes = {'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}
    values = [4.0, 5.0, 6.0]
    return Long(index=indexes, value=values)

@pytest.fixture
def long_obj_with_list_dt():
    # create an Long object for testing
    indexes = {'one':list(np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]'))}
    values = [4.0, 5.0, 6.0]
    return Long(index=indexes, value=values)

@pytest.fixture
def long_obj_with_2d_dt():
    # create an Long object for testing
    indexes = {'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]'), 'two':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}
    values = [4.0, 5.0, 6.0]
    return Long(index=indexes, value=values)

def test_get_item_datetime64(long_obj_with_dt):
    actual = long_obj_with_dt['one', list(np.array(['2022-11-23'], dtype='datetime64[ns]'))]
    expected = Long({'one': np.array(['2022-11-23'], dtype='datetime64[ns]')},[6.0])
    assert expected == actual

def test_get_item_ndarray(long_obj_with_dt):
    actual = long_obj_with_dt['one', np.array(['2022-11-23'], dtype='datetime64[ns]')]
    expected = Long({'one': np.array(['2022-11-23'], dtype='datetime64[ns]')},[6.0])
    assert expected == actual

def test_get_item_list_string(long_obj_with_str):
    actual = long_obj_with_str['one', ['ccc']]
    expected = Long({'one': ['ccc']},[6.0])
    assert expected == actual

def test_get_item_list_int(long_obj_with_int):
    actual = long_obj_with_int['one', [1, 3]]
    expected = Long({'one': [1, 3]},[4.0, 6.0])
    assert expected == actual

def test_get_item_list_slice(long_obj_with_int):
    actual = long_obj_with_int['one', 3:]
    expected = Long({'one': [3, 5]}, [6.0, 7.0])
    assert expected == actual

def test_index(long_obj_with_dt):
    actual = long_obj_with_dt.index
    expected = {'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}
    assert all(np.array_equal(act, exp) for act, exp in zip(actual, expected))
    
def test_value(long_obj_with_dt):  
    actual = long_obj_with_dt.value
    expected = np.array([4.0, 5.0, 6.0])
    assert np.array_equal(expected,actual)
 
def test_dims(long_obj_with_str):
    actual = long_obj_with_str.dims
    expected = ['one']
    assert expected == actual
 
def test_size(long_obj_with_dt):
    actual = long_obj_with_dt.size
    expected = 3
    assert expected == actual
 
def test_ndim(long_obj_with_str):
    actual = long_obj_with_str.ndim
    expected = 1
    assert expected == actual

def test_insert_dict_and_list(long_obj_with_list_dt):
    actual = long_obj_with_list_dt.insert(two={'one':[np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]'), np.array(['2022-11-16', '2022-11-17','2022-11-18'], dtype='datetime64[ns]')]})
    expected = Long({'two':list(np.array(['2022-11-16', '2022-11-17','2022-11-18'], dtype='datetime64[ns]')),'one':list(np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]'))}, [4.0, 5.0, 6.0])
    assert expected == actual

def test_rename(long_obj_with_dt):
    actual = long_obj_with_dt.rename(one='two')
    expected = Long({'two':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    assert expected == actual

def test_drop(long_obj_with_2d_dt):
    actual = long_obj_with_2d_dt.drop('one')
    expected = Long({'two':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    assert expected == actual

def test_items(long_obj_with_dt):
    actual = list(long_obj_with_dt.items())
    expected = [('one',np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')),('value', np.array([4.0, 5.0, 6.0]))]
    assert all(act[0] == exp[0] for act, exp in zip(actual, expected))
    assert all(np.array_equal(act[1], exp[1]) for act, exp in zip(actual, expected))

def test_eq_long():
    A_long = Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    B_long = Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    assert A_long == B_long

def test_ne_long_by_dim():
    A_long = Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    B_long = Long({'two':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    assert A_long != B_long

def test_ne_long_by_dim_value():
    A_long = Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    B_long = Long({'one':np.array(['2022-11-27', '2022-11-27','2022-11-27'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    assert A_long != B_long

def test_ne_long_by_value():
    A_long = Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, 6.0])
    B_long = Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [1.0, 1.0, 1.0])
    assert A_long != B_long

def test_eq_value_float(long_obj_with_dt):
    actual = long_obj_with_dt == 5.0
    expected = np.array([False,True,False])
    assert np.array_equal(expected,actual)

def test_eq_value_int(long_obj_with_dt):
    actual = long_obj_with_dt == 5
    expected = np.array([False,True,False])
    assert np.array_equal(expected,actual)

def test_eq_value_nan():
    long = Long({'one':np.array(['2022-11-25', '2022-11-24','2022-11-23'], dtype='datetime64[ns]')}, [4.0, 5.0, np.nan])
    actual = long == np.nan
    expected = np.array([False,False,True])
    assert np.array_equal(expected,actual)




'''
insert

These tests cover different scenarios such as inserting a new dimension with integer values, 
inserting a new dimension that maps to an existing dimension using a dictionary or a list, 
inserting a new dimension with missing or duplicate values, and inserting a new dimension 
with an invalid type.
'''

@pytest.fixture
def array_obj():
    # create an Array object for testing
    value = [1.0, 2.0, 3.0]
    index = {'x':[1, 2, 3],'y':['a','b','c']}
    data = (index,value)
    coords = {'x': np.array([1, 2, 3]), 'y': np.array(['a', 'b', 'c'])}
    return Array(data=data, coords=coords)

def test_insert_new_dim_int(array_obj):
    # Test inserting a new dimension with integer values
    new_data = {'z':  99}
    new_array = array_obj.insert(**new_data)
    expected_coords = {'x': np.array([1, 2, 3]), 'y': np.array(['a', 'b', 'c']), 'z': np.array([99], dtype=np.int64)}
    assert_array_equal(new_array.coords['z'], expected_coords['z'])
    assert new_array.dims == ['z', 'x', 'y']

def test_insert_new_dim_str(array_obj):
    # Test inserting a new dimension with integer values
    new_data = {'z':  'kkk'}
    new_array = array_obj.insert(**new_data)
    expected_coords = {'z': np.array(['kkk'], dtype=np.object_), 'x': np.array([1, 2, 3]), 'y': np.array(['a', 'b', 'c'])}
    assert_array_equal(new_array.coords['z'], expected_coords['z'])
    assert new_array.dims == ['z', 'x', 'y']

def test_insert_existing_dim_dict(array_obj):
    # Test inserting a new dimension that maps to an existing dimension using a dictionary
    new_data = {'z': {'y': {'a':1, 'b': 2, 'c': 3}}}
    new_array = array_obj.insert(**new_data)
    expected_coords = {'z': np.array([1, 2, 3], dtype=np.int64), 'x': np.array([1, 2, 3]), 'y': np.array(['a', 'b', 'c'])}
    assert_array_equal(new_array.coords['z'], expected_coords['z'])
    assert new_array.dims == ['z', 'x', 'y']

def test_insert_existing_dim_list(array_obj):
    # Test inserting a new dimension that maps to an existing dimension using a list
    new_data = {'z': {'y': [['a', 'b', 'c'], [1, 2, 3]]}}
    new_array = array_obj.insert(**new_data)
    expected_coords = {'z': np.array([1, 2, 3], dtype=np.int64), 'x': np.array([1, 2, 3]), 'y': np.array(['a', 'b', 'c'])}
    assert_array_equal(new_array.coords['z'], expected_coords['z'])
    assert new_array.dims == ['z', 'x', 'y']

def test_insert_existing_dim_duplicate(array_obj):
    # Test inserting a new dimension that maps to an existing dimension with duplicate values
    new_data = {'z': {'y': {'a': 2, 'b': 2, 'c': 2}}}
    new_array = array_obj.insert(**new_data)
    expected_coords = {'z': np.array([2], dtype=np.int64), 'x': np.array([1, 2, 3]), 'y': np.array(['a', 'b', 'c'])}
    assert_array_equal(new_array.coords['z'], expected_coords['z'])
    assert new_array.dims == ['z', 'x', 'y']

def test_insert_existing_dim_error(array_obj):
    # Test inserting a new dimension that maps to an existing dimension with missing values
    with pytest.raises(AssertionError):
        new_data = {'z': {'y': {'b': 2}}}
        array_obj.insert(**new_data)

def test_insert_float_invalid_type_error(array_obj):
    # Test inserting a new dimension with invalid type: Float
    with pytest.raises(AssertionError):
        new_data = {'z': 5.0}
        array_obj.insert(**new_data)

def test_insert_ndarray_invalid_type_error(array_obj):
    # Test inserting a new dimension with invalid type: ndarray
    with pytest.raises(AssertionError):
        new_data = {'z':  np.array([4, 5, 6])}
        array_obj.insert(**new_data)



'''
choice

Sampling from an Array object.

'''

@pytest.fixture
def prob_array():
    # create an Array object for testing
    index = dict(week=[0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3],
                day=[0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1],
                trip=[1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3])

    value = [0.1,0.3,0.6,
            0.5,0.3,0.2,
            0.6,0.1,0.3,
            0.2,0.7,0.1,
            0.4,0.4,0.2,
            0.7,0.3,0.0,
            0.6,0.1,0.3,
            0.2,0.7,0.1,
            ]
    data = (index,value)
    return Array(data=data)


def test_choice(prob_array):
    
    dim = 'trip'
    new_array = prob_array.choice(dim, seed=1)

    index = {'week': np.array([0, 0, 1, 1, 2, 2, 3, 3]),
            'day': np.array([0, 1, 0, 1, 0, 1, 0, 1]),
            'trip': np.array([3, 3, 1, 3, 1, 1, 3, 2])}
    value = np.array([ True,  True,  True,  True,  True,  True,  True,  True])
    expected_array = Array(data=(index,value))

    assert (expected_array == new_array).all()