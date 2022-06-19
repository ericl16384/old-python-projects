"""Author: Russell Lewis

   Provides the Piece class, which models a single square in the map (or, a piece which
   has not yet been placed), and functions for drawing the map.
   """

import sys
import random
from graphics import graphics   # utility by Ben Dicken, wrapper around tkinter


GRID_SIZE = 100


class Piece:
    def __init__(self, top,right,bottom,left, center=""):
        self._top     = top
        self._right   = right
        self._bottom  = bottom
        self._left    = left
        self._center = center

    def __str__(self):
        return "Piece(top={}, right={}, bottom={}, left={}, center={})".format(
                self._top, self._right, self._bottom, self._left, self._center)

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



def random_piece():
    sides = []
    for i in range(4):
        choice = random.randint(1,8)
        if choice <= 5:
            if random.randint(0,1) == 1:
                sides.append("grass")
            else:
                sides.append("grass/road")
        elif choice <= 9:
            sides.append("city")
#        else:
#            sides.append("river")

#    center = random.randint(0,10)
#    if center in (7,8):
#        center = "village"
#    elif center == 9:
#        center = "monastery"
#    else:
#        center = ""

    # if there are exactly 1 or more than 2 roads, then add a village
    # in the center.  Whoops...only do that if there isn't a city!

    road_count = sum(1 if '/' in s    else 0 for s in sides)
    city_count = sum(1 if s == "city" else 0 for s in sides)
    if city_count == 0 and (road_count == 1 or road_count > 2):
        center = "village"
    else:
        center = ""

    return Piece(sides[0], sides[1], sides[2], sides[3], center)



def draw_map(grid, highlight=frozenset(), GRID_SIZE = 100):
    wid = len(grid)
    #print("The grid appears to be {} blocks wide.".format(wid))
    assert wid > 0

    hei = len(grid[0])
    #print("The grid appears to be {} blocks high.".format(hei))
    assert hei > 0
    for i in range(1,wid):
        assert len(grid[i]) == hei, "The length of sublist {} is not the same as the length of sublist 0".format(i)

    window = graphics(GRID_SIZE*wid, GRID_SIZE*hei, "Carcassonne Map")
    window.clear()

    for x in range(wid):
        for y in range(hei):
            left   = x*GRID_SIZE+1
            top    = y*GRID_SIZE+1
            right  = left + GRID_SIZE-2
            bottom = top  + GRID_SIZE-2
            centerX = left + (GRID_SIZE-2)//2
            centerY = top  + (GRID_SIZE-2)//2

            if grid[x][y] is None:
                window.rectangle(left+1,top+1, GRID_SIZE-3,GRID_SIZE-3, fill="light gray")

            else:
                def draw_side(terrain, x1,y1, x2,y2):
                    x3 = centerX
                    y3 = centerY

                    terrain = terrain.split('/')
                    terrain_base = terrain[0]
                    if len(terrain) > 1:
                        assert terrain[1:] == ["road"], terrain
                        road = True
                    else:
                        road = False

                    color_map = {"grass":"green",
                                "river":"blue",
                                "city" :"#A52A2A"}  # brown
                    window.triangle(x1,y1, x2,y2, x3,y3, fill=color_map[terrain_base])

                    if road:
                        window.line((x1+x2)//2, (y1+y2)//2, centerX,centerY, fill="white", width=3)

                piece = grid[x][y]
                draw_side(piece.get_top(),    left, top,    right,top)
                draw_side(piece.get_right(),  right,top,    right,bottom)
                draw_side(piece.get_bottom(), left, bottom, right,bottom)
                draw_side(piece.get_left(),   left, top,    left, bottom)

                radius = GRID_SIZE//6   # size of the center feature
                if piece.get_center() == "village":
                    window.rectangle(centerX-radius, centerY-radius, radius*2,radius*2, fill="yellow")
                if piece.get_center() == "monastery":
                    window.rectangle(centerX-radius, centerY-radius, radius*2,radius*2, fill="red")

            color = "black"
            width = 1
            if (x,y) in highlight:
                color = "red"
                width = 8
                left   += 12
                right  -= 12
                top    += 12
                bottom -= 12

            window.line(left ,top,    right,top,    fill=color, width=width)
            window.line(left ,bottom, right,bottom, fill=color, width=width)
            window.line(left ,top,    left ,bottom, fill=color, width=width)
            window.line(right,top,    right,bottom, fill=color, width=width)

    kill_wind = lambda e: window.primary.destroy()
    kill_prog = lambda e: sys.exit(1)

    window.canvas.bind("<Return>",    kill_wind)
    window.canvas.bind("<Escape>",    kill_wind)
    window.canvas.bind("<Control-c>", kill_prog)

    window.primary.update()
    window.primary.mainloop()
    return



def main():
    map = [[None,None,None], [None,None,None], [None,None,None]]
    map[0][1] = Piece("grass/road", "river", "city", "grass/road")
    map[0][2] = Piece("city", "grass/road", "city", "city")
    map[1][2] = Piece("grass", "grass/road", "grass", "grass/road")
    map[2][2] = Piece("grass", "grass", "grass", "grass/road", center="village")
    map[2][1] = Piece("grass", "grass", "grass", "grass", center="monastery")
    draw_map(map)

    draw_map(map, {(2,1),(0,0)})

    draw_random_map()

def draw_random_map():
    WID = 8
    HEI = 8

    board = []
    for i in range(HEI):
        board.append([])
        for j in range(WID):
            board[-1].append(random_piece())
    draw_map(board)

    board = [[None,None,None],[None,None,None],[None,None,None]]
    board[1][1] = Piece("city", "grass/road", "grass", "grass/road")
    draw_map(board)

if __name__ == "__main__":
    main()


