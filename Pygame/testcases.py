# Imports

from graphics import *
from maths import *
import physics0


# Set up testificates

x = Vector(1, 0)
y = Vector(0, 1)

a = Vector(2, 3)
b = Vector(4, 5)
c = Vector(1, 2)

xy = Matrix(x, y)
abc = Matrix(a, b, c)

rotators = [rotationMatrix(i*45) for i in range(8)]


# Testcases

assert a == Vector(2, 3)
assert b == Vector(4, 5)
assert c == Vector(1, 2)
assert x == Vector(1, 0)
assert y == Vector(0, 1)

assert a+b == Vector(6, 8)
assert a*b == 23

assert (rotators[0]@c).rounded(8) == Vector(1, 2)
assert (rotators[1]@c).rounded(8) == Vector(-0.70710678, 2.12132034)
assert (rotators[2]@c).rounded(8) == Vector(-2, 1)
assert (rotators[3]@c).rounded(8) == Vector(-2.12132034, -0.70710678)
assert (rotators[4]@c).rounded(8) == Vector(-1, -2)
assert (rotators[5]@c).rounded(8) == Vector(0.70710678, -2.12132034)
assert (rotators[6]@c).rounded(8) == Vector(2, -1)
assert (rotators[7]@c).rounded(8) == Vector(2.12132034, 0.70710678)

assert abc.offset(x) == Matrix(
    (3, 5, 2),
    (3, 5, 2)
)
assert abc.offset(y) == Matrix(
    (2, 4, 1),
    (4, 6, 3)
)

assert str(abc) == """<Matrix 3x2
    2, 4, 1
    3, 5, 2
>"""

assert abc.bounds() == Matrix(
    Vector(1, 2),
    Vector(4, 5)
)

assert not abc.copy() is abc
assert not abc.copy().vectors is abc.vectors
assert abc.copy() == abc

assert xy@abc == abc
assert abc@xy == Matrix(*abc[:-1])

assert a.rows() == ((2,), (3,))
assert abc.rows() == ((2, 4, 1), (3, 5, 2))

assert a-b == Vector(-2, -2)

assert abs(-a) == a
assert abs(-abc) == abc

assert a.resize(3) == Vector(2, 3, 0)
assert a.resize(1) == Vector(2)

assert abc.resize(4, 3) == Matrix(
    (2, 4, 1, 0),
    (3, 5, 2, 0),
    (0, 0, 0, 0)
)
assert abc.resize(2, 1) == Matrix(
    (2, 4)
)

assert a.rotate(90).rounded() == Vector(-3, 2)
assert abc.rotate(90).rounded() == Matrix(
    Vector(-3, 2),
    Vector(-5, 4),
    Vector(-2, 1)
)

assert round(a.magnitude(), 8) == 3.60555128

# Description

if __name__ == "__main__":
    print("TESTCASES PASSED")
    print(f"{os.path.basename(__file__)} is a library of testcases in progress made by Eric Lewis.")
