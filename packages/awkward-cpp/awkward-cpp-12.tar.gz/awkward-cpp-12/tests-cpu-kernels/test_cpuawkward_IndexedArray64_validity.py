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

def test_cpuawkward_IndexedArray64_validity_1():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_2():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_3():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_4():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_5():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_6():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_7():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_8():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_9():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_10():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_11():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_12():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_13():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_14():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_15():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_16():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_17():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_18():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_19():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_20():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray64_validity_21():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_22():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_23():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_24():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray64_validity_25():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int64*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

