"""Author: Eric Lewis

   Expanded edition on carcassonne_display. (Currently relies on the original.)
   """

#from carcassonne_display import Piece as createPiece
from carcassonne_display import random_piece as randomPiece
from carcassonne_display import draw_map

import random

grass = "grass"
road = "grass/road"
city = "city"
town = "village"
monastery = "monastery"

class createPiece:
    def __init__(self, top, right, bottom, left, center = "", walls = [False]*4):
        self._top = top
        self._right = right
        self._bottom = bottom
        self._left = left
        self._center = center
        self._walls = walls

    def __str__(self):
        return "createPiece(top={}, right={}, bottom={}, left={}, center={}, walls={})".format(
            self._top, self._right, self._bottom, self._left, self._center, self._walls)

    def get_top(self):
        return self._top
    def get_right(self):
        return self._right
    def get_bottom(self):
        return self._bottom
    def get_left(self):
        return self._left
    def get_center(self):
        return self._center
    def get_walls(self):
        return self._separators

def rotatePiece(piece,rotations): # Rotation is 90 degree increments, counterclockwise
    rotations %= 4

    if rotations == 0:
        return piece

    past = createPiece(piece.get_left(), piece.get_top(), piece.get_right(), piece.get_bottom(), piece.get_center())
    for i in range(rotations+1):
        present = createPiece(past.get_right(), past.get_bottom(), past.get_left(), past.get_top(), past.get_center())
        past = present
    return past

class map:
    def __init__(self, content=[[None]*3, [None, createPiece(city, road, grass, road), None], [None]*3]):
        self.map = content
    def get_map(self):
        return self.map
    def findFittingRotations(self, originalPiece, location):
        successes = []
        for i in range(4):
            piece = rotatePiece(originalPiece, i)

            successes.append(i)

            #Right
            print()
            if self.map[location[0]][location[1]] == None:
                print("First saftey passed")
                if not location[0] == len(self.map)-1:
                    print("Second saftey passed")
                    if not self.map[location[0]+1][location[1]] == None:
                        print("Third saftey passed")
                        if not piece.get_right == self.map[location[0]+1][location[1]].get_left:
                            print("Negative")
                            successes.pop()
                            continue
            #Top
            if False:
                continue
            #Left
            if False:
                continue
            #Bottom
            if False:
                continue
        return successes
    def findAvailableMoves(self, piece):
        return []
    def edit(self, piece, location):
        self.map[location[0]][location[1]] = piece

        # +x expansion
        if not self.map[-1] == [None]*len(self.map[0]):
            self.map.append([None]*len(self.map[0]))

        # -x expansion
        if not self.map[0] == [None]*len(self.map[0]):
            self.map.insert(0, [None]*len(self.map[0]))

        # +y expansion
        loopBool = False
        for i in range(len(self.map)):
            if not self.map[i][-1] == None:
                loopBool = True
                break
        if loopBool:
            for i in range(len(self.map)):
                self.map[i].append(None)

        # -y expansion
        loopBool = False
        for i in range(len(self.map)):
            if not self.map[i][0] == None:
                loopBool = True
                break
        if loopBool:
            for i in range(len(self.map)):
                self.map[i].insert(0, None)

        #This part is not neccessary, but I feel it will help solve "house rules" expansions

        # +x reduction
        if self.map[-2] == [None]*len(self.map[0]) and len(self.map) > 3:
            self.map.pop()

        # -x reduction
        if self.map[1] == [None]*len(self.map[0]) and len(self.map) > 3:
            self.map.pop(0)

        # +y reduction
        loopBool = True
        for i in range(len(self.map)):
            if not self.map[i][-2] == None:
                loopBool = False
                break
        if loopBool and len(self.map[0]) > 3:
            for i in range(len(self.map)):
                self.map[i].pop()

        #-y reduction
        loopBool = True
        for i in range(len(self.map)):
            if not self.map[i][1] == None:
                loopBool = False
                break
        if loopBool and len(self.map[0]) > 3:
            for i in range(len(self.map)):
                self.map[i].pop(0)

    def draw(self, highlight=frozenset()):
        draw_map(self.map, highlight, GRID_SIZE=50)



if __name__ == "__main__":
    map = map()
    map.draw()

    print(map.findFittingRotations(createPiece(road, road, road, road), [0,1]))

    map.edit(createPiece(road, road, road, road), [0,1])
    map.draw()

    #while True:
    #    map.draw()
    #    map.edit(randomPiece(), [random.randint(0,len(map.get_map())-1),random.randint(0,len(map.get_map()[0])-1)])
