# Imports

import copy, math, os


# Functions

def circlePos(angle):
    "Angle is in degrees"
    angle = math.radians(angle)
    return Vector(math.cos(angle), math.sin(angle))

# Matrix-vector functions

def rotationMatrix(angle):
    "Angle is in degrees"
    angle = math.radians(angle)
    return Matrix(
        (math.cos(angle), -math.sin(angle)),
        (math.sin(angle), math.cos(angle))
    )


# Classes

class Vector:
    keyShortcuts = {
        "x": 0,
        "y": 1,
        "z": 2
    }

    def __init__(self, *components):
        "Any whole number of dimensions is supported"

        if isinstance(components, self.__class__):
            components = components.get()

        # Convert vectors to a new tuple
        components = copy.deepcopy(tuple(components))

        # Assertion
        for i in components:
            assert isinstance(i, (int, float)), components
        
        # Confirm
        self.components = components
    def __str__(self):
        return f"<{self.__class__.__name__} 1x{len(self)} {list(self.get())}>"
    def __len__(self):
        return len(self.components)
    def __getitem__(self, key):
        try:
            if key in self.__class__.keyShortcuts:
                return self.components[self.__class__.keyShortcuts[key]]
            else:
            #elif key in self.components:
                return self.components[key]
            #else:
            #    return 0
        except TypeError:
            return self.vectors[key]
    #def __setitem__(self, key, value):
    #    if key in self.__class__.keyShortcuts:
    #        self.components[self.__class__.keyShortcuts[key]] = value
    #    else:
    #        self.components[key] = value
    
    def __add__(self, other):
        assert isinstance(other, self.__class__), type(other).__name__+" not supported"

        # Can't use zip, as a vector may be bigger than the other
        components = []
        i = 0
        while i < len(self) or i < len(other):
            if i < len(self):
                a = self[i]
            else:
                a = 0
            if i < len(other):
                b = other[i]
            else:
                b = 0
            i += 1

            components.append(a+b)
        return self.__class__(*components)
    def __sub__(self, other):
        return self + -other
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.dotProduct(other)
        elif isinstance(other, Matrix):
            raise Exception("use matrix multiplication via \"@\"")
        else:
            return self.__class__(*[i*other for i in self.components])
    def __neg__(self):
        return self * -1

    def __matmul__(self, other):
        if isinstance(other, Vector):
            return self.crossProduct(other)
        elif isinstance(other, Matrix):
            raise Exception("use matrix@vector, not vector@matrix")
        else:
            raise Exception("use regular multiplication via \"*\"")
    
    def __truediv__(self, other):
        return self.__class__(*[i/other for i in self.components])
    def __floordiv__(self, other):
        return self.__class__(*[i//other for i in self.components])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.components == other.components
    def __ne__(self, other):
        return not self == other

    def __abs__(self):
        return self.__class__(*[abs(i) for i in self])

    def dotProduct(self, other):
        # Can use zip, as anything times 0 = 0, so extra dimensions don't matter
        return sum([i*j for i, j in zip(self.components, other.components)])
    def crossProduct(self, other):
        raise NotImplementedError
    
    def get(self):
        return copy.deepcopy(self.components)
    def copy(self):
        return self.__class__(*self.components)
    def rounded(self, ndigits=None):
        return self.__class__(*[round(i, ndigits) for i in self.components])
    def rows(self):
        return tuple((i,) for i in self)
    def sum(self):
        return sum(self.components)
    def resize(self, height):
        return self.__class__(
            * list(self.components[:height]) + [0 for i in range(height-len(self))]
        )
    def rotate(self, angle):
        "Angle is in degrees"
        return rotationMatrix(angle)@self
    def magnitude(self):
        # Pythagorean Theorum
        return math.sqrt(sum([i**2 for i in self.components]))

class Matrix:
    # Sum doesn't work for some reason, because it tries 0 + Vector, so use self.sum()

    keyShortcuts = {
        "i": 0,
        "j": 1,
        "k": 2
    }

    def __init__(self, *vectors):
        """Any whole number of vectors is supported.
        If *vectors is a Matrix, they are assumed to be column vectors.
        If *vectors is a tuple or list of tuples or lists, they will be reformatted to a list of (column) Vectors.
        Example:
        Matrix(
            (1, 2),
            (3, 4)
        ) == Matrix(Vector(1, 3), Vector(2, 4))"""

        # Convert vectors to a new tuple
        #if isinstance(vectors, self.__class__):
        #vectors = copy.deepcopy(tuple(vectors))

        # Make sure all vectors are the same size
        for i in range(len(vectors)):
            for j in range(i+1, len(vectors)):
                assert len(vectors[i]) == len(vectors[j]), f"{len(vectors[i])} != {len(vectors[j])}"

        if isinstance(vectors[0], Vector):
            vectors = [Vector(*i) for i in vectors]
        else:
            # Will be coming in in rows, so reformat at shown in documentation
            vectors = [Vector(*i) for i in zip(*vectors)]
        
        # Convert vectors to a new tuple
        self.vectors = copy.deepcopy(tuple(vectors))

        # Init size
        self.width, self.height = len(self.vectors), len(self.vectors[0])
    def __str__(self):
        out = "<"
        out += self.__class__.__name__ + " "
        out += str(self.width) + "x" + str(self.height)
        out += "\n"
        for i in self.rows(): #zip(*self.get()):
            out += " "*4 + str(list(i))[1:-1] + "\n"
        out += ">"
        return out
    def __len__(self):
        return self.getWidth()
    def __getitem__(self, key):
        try:
            if key in self.__class__.keyShortcuts:
                return self.vectors[self.__class__.keyShortcuts[key]]
            else:
            #elif key in self.vectors:
                return self.vectors[key]
            #else:
            #    return Vector()
        except TypeError:
            return self.vectors[key]
    #def __setitem__(self, key, value):
    #    self.vectors[key] = value

    def __add__(self, other):
        raise NotImplementedError
    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        return self.__class__(*[i*other for i in self])
    def __neg__(self):
        return self * -1
    
    def __matmul__(self, other):
        if isinstance(other, Vector):
            out = Vector()
            # Can use zip, as anything times 0 = 0, so extra dimensions don't matter
            for i, j in zip(self, other):
                out += i*j
            return out
                
        elif isinstance(other, Matrix):
            return self.__class__(*[self@i for i in other])

        else:
            raise Exception("use regular multiplication via \"*\"")

    def __truediv__(self, other):
        raise NotImplementedError
    def  __floordiv__(self, other):
        raise NotImplementedError
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.vectors == other.vectors
    def __ne__(self, other):
        return not self == other

    def __abs__(self):
        return self.__class__(*[abs(i) for i in self])

    def get(self):
        return tuple([i.get() for i in self.vectors])
    def copy(self):
        return self.__class__(*self)
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def rounded(self, ndigits=None):
        return self.__class__(*[i.rounded(ndigits) for i in self.vectors])
    def offset(self, amount:Vector):
        return self.__class__(*[i+amount for i in self.vectors])
    def rows(self):
        return tuple(zip(*self))
    def bounds(self):
        # We want a Matrix containing two Vectors, one that is min, one max
        rows = self.rows()
        return Matrix(
            Vector(*[min(i) for i in rows]),
            Vector(*[max(i) for i in rows])
        )
    def sum(self):
        if len(self) == 0:
            return Vector()
        out = self[0]
        for i in range(1, len(self)):
            out += self[i]
        return out
    def resize(self, width=None, height=None):
        if width == None:
            width = self.width
        if height == None:
            height = self.height

        return self.__class__(
            * [i.resize(height) for i in self.vectors][:width] + [Vector(*[0]*height) for i in range(width-len(self))]
        )
    def rotate(self, angle):
        "Angle is in degrees"
        return rotationMatrix(angle)@self

# Description

if __name__ == "__main__":
    print(f"{os.path.basename(__file__)} is a library in progress made by Eric Lewis.")
    input("Press ENTER for contents.")
    print()
    for k, v in globals().copy().items():
        if not k.startswith("__"):
            print(f"{k} = {v}")
