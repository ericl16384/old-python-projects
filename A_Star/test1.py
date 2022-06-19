# Imports

import math


# Classes

class Node:
    # This just smooths out debugging, by making the ids sequential
    id = 0

    def __init__(self, coords=None):
        "data is stored for use by a heuristic (this is usually coords)"
        self.coords = coords

        self.connections = {}
        self.id = self.__class__.id
        self.__class__.id += 1

    def __str__(self):
        # Extra space is so that VSCode stays sane       >|<
        return f"<Node {self.getID()} connected to nodes { {n.getID():d for(n,d) in self.connections.items()}}>"
    
    def getConnections(self):
        return self.connections.copy()
    
    def getID(self):
        return self.id
    

    def connect(self, other, distance):
        # If distance is special
        if distance == None:
            if self.coords == None:
                raise ValueError("Node needs to have coords when distance is None")
            elif other.coords == None:
                raise ValueError("Other node needs to have coords when distance is None")
            else:
                # Pythagorean Theorum
                distance = math.sqrt(sum([
                    (a-b)**2
                for a, b in zip(self.coords, other.coords)]))
        
        self.connections[other] = distance
    
    def link(self, other, distance):
        self.connect(other, distance)
        other.connect(self, distance)
    
    def grow(self, quantity, distance):
        nodes = [self.__class__() for i in range(quantity)]
        for node in nodes:
            self.link(node, distance)
        return nodes
    

    def disconnect(self, other):
        try:
            self.connections.pop(other)
        except KeyError:
            return False

    def unlink(self, other):
        self.disconnect(other)
        other.disconnect(self)

    def empty(self):
        # Can't change the size of an iterable while iterating, so this is in two steps
        for node in [i for i in self.connections.keys()]:
            self.unlink(node)
    

    def getCoords(self):
        return self.coords.copy()
    
    def setCoords(self, coords):
        self.coords = coords


# A*

def A_Star(start, end):
    #new = {}
    #old = {start}

    while True:
        break


# Testcase

nodes = [Node() for i in range(3)] # Can't do [Node()]*3 because it copies the reference

nodes[0].link(nodes[1], 3)
nodes[1].link(nodes[2], 4)
nodes[2].link(nodes[0], 5)

nodes.extend(nodes[-1].grow(2, 10))




















for node in nodes:
    print(node)
