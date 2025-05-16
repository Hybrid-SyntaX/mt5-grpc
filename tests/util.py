import logging
from typing import Literal

import numpy as np
import pytest


def assert_lists_are_equal(list1, list2, direction: Literal['left', 'right'] = 'right'):
    assert type(list1) == type(list2)
    assert len(list1) == len(list2), f"Mismatch in length: {len(list1)} vs {len(list2)}"

    attrs = get_public_attributes(list1[0]) if direction == 'left' else get_public_attributes(list2[0])

    for left, right in zip(list1, list2):
        for attr_name in attrs:
            lattr_value = getattr(left, attr_name)
            rattr_value = getattr(right, attr_name)
            assert lattr_value == rattr_value, f"Mismatch in {attr_name}: {lattr_value} vs {rattr_value}"

def assert_values_are_equal(obj1, obj2, direction: Literal['left', 'right'] = 'right',exclude:list=[], approximate:list=[]):
    attrs = get_public_attributes(obj1) if direction == 'left' else  get_public_attributes(obj2)
    attrs = [a for a in attrs if a not in exclude]
    for attr_name in attrs:
        lattr_value = getattr(obj1, attr_name)
        rattr_value = getattr(obj2, attr_name)
        if attr_name in approximate:
            assert lattr_value == pytest.approx(rattr_value), f"Mismatch in {attr_name}: {lattr_value} vs {rattr_value}"
            logging.warning(f'pytest.approx was used on {attr_name}: original value: {rattr_value}, approx value: {pytest.approx(rattr_value)}')
        else:
            assert lattr_value == rattr_value, f"Mismatch in {attr_name}: {lattr_value} vs {rattr_value}"

def assert_numpy_ndarray_are_equal(expected,actual):
    assert type(expected) == type(actual)
    assert expected.dtype == actual.dtype
    assert np.array_equal(expected, actual)

def get_public_attributes(obj):
    return [a for a in dir(obj) if not a.startswith('_') and not callable(getattr(obj, a))]