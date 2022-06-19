# https://www.youtube.com/watch?v=-L-WgKMFuhE


import json


# Functions
    
def getAdjacent(x, y, sides=True, corners=False):
    # Goes around counterclockwise from angle 0 with sides then corners
    out = []
    if sides:
        out.extend([
            [x+1,   y],
            [x,   y+1],
            [x-1,   y],
            [x,   y-1]
        ])
    if corners:
        out.extend([
            [x+1, y+1],
            [x-1, y+1],
            [x-1, y-1],
            [x+1, y-1]
        ])
    return out


# Classes

class Node(list): # make it not a child class
    def __init__(self, connections=[]):
        for i in connections:
            assert len(i) == 2 # [other, resistance]
        super().__init__(connections)
    
    def connect(self, other, resistance):
        for i in self:
            if i[0] == other:
                return

        self.append([other, resistance])
    
    def link(self, other, resistance):
        # Connect the nodes
        self.connect(other, resistance)
        other.connect(self, resistance)
    
    def __str__(self):
        return f"<Node {id(self)} with connections: {str([id(i) for i in self])}>"

class Tile: # package for nodes
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.node = Node()

class Grid:
    def __init__(self, tiles=[]):
        self.bounds = None
        self.nodes = {}

        self.add(tiles)
    
    def getNodes(self):
        out = []
        for x in self.nodes.keys():
            for y in self.nodes[x].keys():
                out.append(self.nodes[x][y])
        return out
    
    def add(self, tiles, force=False): # make it tile singular
        assert len(tiles) > 0

        if self.bounds == None:
            self.bounds = [
                [tiles[0].x, tiles[0].y],
                [tiles[0].x, tiles[0].y]
            ]

        for tile in tiles:
            # Shorthand
            x = tile.x
            y = tile.y
            node = tile.node

            # Expand bounds to fit
            self.bounds[0][0] = min(self.bounds[0][0], x)
            self.bounds[0][1] = min(self.bounds[0][1], y)
            self.bounds[1][0] = max(self.bounds[1][0], x)
            self.bounds[1][1] = max(self.bounds[1][1], y)

            # Format the nodemap
            if x not in self.nodes.keys():
                self.nodes[x] = {}
            
            # Ignore if not force
            if y in self.nodes[x].keys() and not force:
                continue

            # Add the tile
            self.nodes[x][y] = node


            # Connect (append) nodes NOT FINISHED

            # Right
            #if x+1 in self.nodes.keys() and y in self.nodes[x+1].keys():
            #    tile.node.link(self.nodes[x+1][y])

            for i in getAdjacent(x, y):
                try:
                    self.nodes[x][y].link(self.nodes[i[0]][i[1]], 10)
                except KeyError:
                    pass

    #def fill(self, x1, y1, x2, y2):
    #    assert x1 <= x2
    #    assert y1 <= y2

    #    for x in range(x1, x2+1):
    #        for y in range(y1, y2+1):
    #            self.add([Tile(x, y)])

    def __str__(self):
        out = ""

        # max y to min y
        for y in range(self.bounds[1][1], self.bounds[0][1]-1, -1):
            # min x to max x
            for x in range(self.bounds[0][0], self.bounds[1][0]+1):
                # Empty
                if not x in self.nodes.keys() or not y in self.nodes[x].keys():
                    out += "  "
                    continue
                # Regular
                out += "██"
            if not y == self.bounds[0][1]:
                out += "\n"
        
        return out


# Code

a = Tile(0, 0)
b = Tile(1, 0)
map = Grid([a, b])

new = []
known = []
new.append(a)


# Test

print(new)
print(known)
print(map)
with open("data.txt", "w") as f:
    print(json.dumps([str(i) for i in map.getNodes()], indent=4), file=f)
