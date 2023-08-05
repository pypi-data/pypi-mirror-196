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

def test_cpuawkward_ListArray_fill_to64_from32_1():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    tostopsoffset = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [123, 123, 123, 5.0, 3.0, 5.0]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 6.0, 5.0, 7.0]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_cpuawkward_ListArray_fill_to64_from32_2():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    tostopsoffset = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [123, 123, 123, 4.0, 3.0, 3.0]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 11.0, 7.0, 8.0]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_cpuawkward_ListArray_fill_to64_from32_3():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    tostopsoffset = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [123, 123, 123, 4.0, 7.0, 8.0]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 4.0, 7.0, 8.0]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_cpuawkward_ListArray_fill_to64_from32_4():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    tostopsoffset = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [123, 123, 123, 4.0, 10.0, 9.0]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 4.0, 12.0, 9.0]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_cpuawkward_ListArray_fill_to64_from32_5():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    tostopsoffset = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [123, 123, 123, 3.0, 3.0, 3.0]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 4.0, 4.0, 4.0]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

