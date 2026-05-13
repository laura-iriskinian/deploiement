import pytest
from calculatrice import add, subtract, multiply, divide


def test_add():
    assert add(2, 3) == 5

def test_add_negatif():
    assert add(-1, -4) == -5

def test_add_zero():
    assert add(0, 7) == 7


def test_subtract():
    assert subtract(10, 4) == 6

def test_subtract_negatif():
    assert subtract(-3, -2) == -1

def test_subtract_zero():
    assert subtract(5, 0) == 5


def test_multiply():
    assert multiply(3, 4) == 12

def test_multiply_negatif():
    assert multiply(-2, 5) == -10

def test_multiply_zero():
    assert multiply(9, 0) == 0


def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_decimal():
    assert divide(1, 4) == 0.25

def test_divide_par_zero():
    with pytest.raises(ValueError, match="Division par zéro impossible"):
        divide(5, 0)
