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

def test_cpuawkward_IndexedArray64_getitem_nextcarry_outindex_64_1():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 2
    funcC = getattr(lib, 'awkward_IndexedArray64_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, toindex, fromindex, lenindex, lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toindex = [0.0, 1.0, 2.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_getitem_nextcarry_outindex_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 2
    funcC = getattr(lib, 'awkward_IndexedArray64_getitem_nextcarry_outindex_64')
    assert funcC(tocarry, toindex, fromindex, lenindex, lencontent).str

def test_cpuawkward_IndexedArray64_getitem_nextcarry_outindex_64_3():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, toindex, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toindex = [0.0, 1.0, 2.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

