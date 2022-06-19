# Imports

from math import *


# Util

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def getMag(self):
        return sqrt(x**2+y**2)

    def norm(self):
        c = self.getMag()

        try:
            return Vector(self.x/c, self.y/c)

        except ZeroDivisionError:
            return Vector(0, 0) # Not correct, but it works

    def setMag(self, mag):
        return self.norm()*mag
    

# Inputs

#mass = 1

point = [-2, 0]

rect = [
    [-1, -1],
    [1, 1]
]

resolution = 1


# Code

def getGravity(x1, y1, x2, y2):
    try:
        return 1/sqrt(abs(x2 - x1) ** 2 + abs(y2 - y1) ** 2)

    except ZeroDivisionError:
        return 1

total = Vector(0, 0)

for x in range(rect[0][0], rect[1][0]+resolution, resolution):
    for y in range(rect[0][1], rect[1][1]+resolution, resolution):
        total += Vector(x, y).setMag(getGravity(point[0], point[1], x, y))

print(total)
