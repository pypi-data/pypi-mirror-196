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

def test_pyawkward_IndexedArray_fill_to64_from64_1():
    toindex = [123, 123, 123, 123, 123, 123]
    toindexoffset = 3
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_from64')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, fromindex=fromindex, length=length, base=base)
    pytest_toindex = [123, 123, 123, 4.0, 3.0, 3.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_from64_2():
    toindex = [123, 123, 123, 123, 123, 123]
    toindexoffset = 3
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_from64')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, fromindex=fromindex, length=length, base=base)
    pytest_toindex = [123, 123, 123, 4.0, 5.0, 5.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_from64_3():
    toindex = [123, 123, 123, 123, 123, 123]
    toindexoffset = 3
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_from64')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, fromindex=fromindex, length=length, base=base)
    pytest_toindex = [123, 123, 123, 4.0, 6.0, 3.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_from64_4():
    toindex = [123, 123, 123, 123, 123, 123]
    toindexoffset = 3
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_from64')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, fromindex=fromindex, length=length, base=base)
    pytest_toindex = [123, 123, 123, 4.0, 7.0, 5.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_from64_5():
    toindex = [123, 123, 123, 123, 123, 123]
    toindexoffset = 3
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_from64')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, fromindex=fromindex, length=length, base=base)
    pytest_toindex = [123, 123, 123, 3.0, 3.0, 3.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

