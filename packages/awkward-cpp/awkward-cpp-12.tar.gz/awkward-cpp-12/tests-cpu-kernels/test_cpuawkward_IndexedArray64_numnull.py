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

def test_cpuawkward_IndexedArray64_numnull_1():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray64_numnull')
    ret_pass = funcC(numnull, fromindex, lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_numnull_2():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray64_numnull')
    ret_pass = funcC(numnull, fromindex, lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_numnull_3():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray64_numnull')
    ret_pass = funcC(numnull, fromindex, lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_numnull_4():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray64_numnull')
    ret_pass = funcC(numnull, fromindex, lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_numnull_5():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray64_numnull')
    ret_pass = funcC(numnull, fromindex, lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

