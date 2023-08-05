# AUTO GENERATED ON 2023-03-07 AT 19:33:13
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import kernels

def test_pyawkward_RegularArray_getitem_next_range_64_1():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    regular_start = 3
    step = 3
    length = 3
    size = 3
    nextsize = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_64')
    funcPy(tocarry=tocarry, regular_start=regular_start, step=step, length=length, size=size, nextsize=nextsize)
    pytest_tocarry = [3, 6, 9, 6, 9, 12, 9, 12, 15]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

