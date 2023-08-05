# AUTO GENERATED ON 2023-03-07 AT 19:33:13
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import pytest

from awkward_cpp.cpu_kernels import lib

def test_cpuawkward_ListArrayU32_getitem_next_range_counts_64_1():
    total = [123]
    total = (ctypes.c_int64*len(total))(*total)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_counts_64')
    ret_pass = funcC(total, fromoffsets, lenstarts)
    pytest_total = [0]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_next_range_counts_64_2():
    total = [123]
    total = (ctypes.c_int64*len(total))(*total)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_counts_64')
    ret_pass = funcC(total, fromoffsets, lenstarts)
    pytest_total = [2]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_next_range_counts_64_3():
    total = [123]
    total = (ctypes.c_int64*len(total))(*total)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_counts_64')
    ret_pass = funcC(total, fromoffsets, lenstarts)
    pytest_total = [-1]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_next_range_counts_64_4():
    total = [123]
    total = (ctypes.c_int64*len(total))(*total)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_counts_64')
    ret_pass = funcC(total, fromoffsets, lenstarts)
    pytest_total = [2]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_next_range_counts_64_5():
    total = [123]
    total = (ctypes.c_int64*len(total))(*total)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_counts_64')
    ret_pass = funcC(total, fromoffsets, lenstarts)
    pytest_total = [0]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)
    assert not ret_pass.str

