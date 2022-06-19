# Imports

import copy, json


# Classes

class StopRecursion(Exception):
    pass


# Init

map = (
    (1, 3, 4, 5, 2, 0),
    (2, 5, 0, 4, 1, 3),
    (0, 1, 3, 2, 5, 4),
    (5, 4, 1, 3, 0, 2),
    (4, 2, 5, 0, 3, 1),
    (3, 0, 2, 1, 4, 5)
)

pieceColors = (
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple"
)


# Assertions

assert len(map) == 6

for row in map:
    assert len(row) == 6
    assert 0 in row
    assert 1 in row
    assert 2 in row
    assert 3 in row
    assert 4 in row
    assert 5 in row

for column in zip(*map):
    assert len(column) == 6
    assert 0 in column
    assert 1 in column
    assert 2 in column
    assert 3 in column
    assert 4 in column
    assert 5 in column

assert len(pieceColors) == 6


# Solve

def recursiveBacktrack(map, placedPieces=None, **meta):
    "map is tuple of tuples and placedPieces is a list of lists or None"


    # Prep

    # Map is not edited
    ## Set up map
    #map = copy.deepcopy(map)

    # Set up placedPieces
    if placedPieces:
        placedPieces = copy.deepcopy(placedPieces)
    else:
        placedPieces = [[None]*len(map)]*len(map)
    
    # Meta
    if meta:
        pieceCount = meta["pieceCount"]
        focusHeight = meta["focusHeight"]
        row = meta["row"]
    
    # Not meta
    else:
        pieceCount = {i: 0 for i in range(len(map))}
        focusHeight = 0
        row = 0

    
    # Solve

    endRow = row
    firstIteration = True
    while not row == endRow or firstIteration:
        # Setup
        firstIteration = False
        mapRow = map[row]
        pieceRow = placedPieces[row]
        
        # If there is an empty space
        if not focusHeight in pieceRow:
            # Try all different colors
            for color in range(len(map)):
                # Put the color in place
                tempRow = copy.deepcopy(placedPieces[row])
                column = mapRow.index(focusHeight)
                tempRow[column] = color

                # DEBUG
                print("map")
                for i in map:
                    print(" "*4+str(i))
                print("pieces")
                for i in placedPieces:
                    print(" "*4+str(i))
                print("focusHeight", focusHeight)
                print("row        ", row)
                print("column     ", column)
                print()

                # If it is already in the column, continue
                invalid = False
                for i in range(len(map)):
                    if placedPieces[i][column] == color:
                        invalid = True
                        break
                if invalid:
                    continue
                else:
                    placedPieces[row] = tempRow

                # recursiveBacktrack()
                try:
                    placedPieces = recursiveBacktrack(map, placedPieces,
                        # meta
                        pieceCount=pieceCount,
                        focusHeight=focusHeight,
                        row=row
                    )
                except StopRecursion as err:
                    bestAttempt = err
                
                # If it is a solution, break
                if placedPieces:
                    break
            break
    
        # Increment
        row = (row+1)%len(map)


    # Return

    if pieceCount == {i: len(map) for i in range(len(map))}:
        return placedPieces
    else:
        try:
            raise bestAttempt
        except NameError:
            out = "Solution not found. Best attempt: "
            for i in placedPieces:
                out += "\n    "+str(i)[1:-1]
            raise StopRecursion(out)

solution = recursiveBacktrack(map)


# Print

print("solution:")
for row in solution:
    print(" "*4+str(row)[1:-1])
