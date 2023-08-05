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

def test_pyawkward_index_rpad_and_clip_axis0_64_1():
    toindex = [123, 123, 123]
    target = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0_64')
    funcPy(toindex=toindex, target=target, length=length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

