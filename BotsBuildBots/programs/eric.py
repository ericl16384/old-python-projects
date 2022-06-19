# Imports

# Standard imports
import random

# Custom imports
import utilities

#def moveTo(x1, y1, x2, y2, xFirst=True):
#    if xFirst:
#        if x1 < x2:
#            return "east"
#        elif x1 > x2:
#            return "west"
#        elif y1 < y2:
#            return "north"
#        elif y1 > y2:
#            return "south"
#    else:
#        if y1 < y2:
#            return "north"
#        elif y1 > y2:
#            return "south"
#        elif x1 < x2:
#            return "east"
#        elif x1 > x2:
#            return "west"
#
#def adjustCoords(coords, direction):
#    if direction == "north":
#        coords[1] += 1
#    elif direction == "south":
#        coords[1] -= 1
#    elif direction == "east":
#        coords[0] += 1
#    elif direction == "west":
#        coords[0] -= 1
#    return coords



class noAI:
    def __init__(self):
        pass
    
    def run(self, taskResponse):
        pass



# Depreciated
def test1(variables, args):
    """args: taskResponse"""
    if args["robot"].getJob() == None:
        return {"output": {
            "task": "move",
            "parameters": random.choice(("north", "south", "east", "west"))#,
            #"queued": random.randint(2, 2)
        }}

class test2:
    def __init__(self):
        pass

    def run(self, taskResponse):
        return {
            "task": "move",
            "parameters": random.choice(("north", "south", "east", "west"))#,
            #"queued": random.randint(2, 2)
        }

# Depreciated
class test3: # Unfinished. Indended to be a spiral out
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = None

    def run(self, taskResponse):
        if self.x > 0:
            if self.x == self.y:
                # North East corner
                if self.direction == "north":
                    self.turnLeft()
                elif self.direction == "east":
                    self.turnRight()
                else:
                    raise ValueError
            elif self.x == self.y*-1:
                # South East corner
                pass
        
        elif self.x < 0:
            if self.x == self.y:
                # South West corner
                pass
            elif self.x == self.y*-1:
                # North West corner
                pass
        
        elif self.x == 0:
            if self.y > 0 or self.y < 0:
                # North or South
                self.direction = random.choice(("east", "west"))
            elif self.y == 0:
                # Start
                self.direction = random.choice(("north", "south", "east", "west"))

        elif self.y == 0 and self.x > 0 or self.x < 0:
            # East or west
            self.direction = random.choice(("north", "south"))
        
        # Keep track of location relative to start
        if self.direction == "north":
            self.y += 1
        elif self.direction == "south":
            self.y -= 1
        elif self.direction == "east":
            self.x += 1
        elif self.direction == "west":
            self.x -= 1

        # Give move command
        return {
            "task": "move",
            "parameters": self.direction
        }

    def turnLeft(self):
        if self.direction == "north":
            self.direction = "west"
        elif self.direction == "west":
            self.direction = "south"
        elif self.direction == "south":
            self.direction = "east"
        elif self.direction == "east":
            self.direction = "north"
        else:
            raise ValueError
        return self.direction
    
    def turnRight(self):
        if self.direction == "north":
            self.direction = "east"
        elif self.direction == "east":
            self.direction = "south"
        elif self.direction == "south":
            self.direction = "west"
        elif self.direction == "west":
            self.direction = "north"
        else:
            raise ValueError
        return self.direction

# Depreciated
class test4:
    def __init__(self):
        self.x = 0
        self.direction = "east"
    
    def run(self, taskResponse):
        # Alternate direction
        if self.x > 3:
            self.direction = "west"
        elif self.x < -3:
            self.direction = "east"
        
        # Keeping track of location relative to start
        if self.direction == "east":
            self.x += 1
        elif self.direction == "west":
            self.x -= 1

        # Give move command
        return {
            "task": "move",
            "parameters": self.direction
        }

# Depreciated
class test5:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = "east"
    
    def run(self, taskResponse):
        # Alternate direction
        if self.x >= 3:
            self.direction = "west"
        elif self.x <= -3:
            self.direction = "east"
        
        # Keeping track of location relative to start
        if self.direction == "east":
            self.x += 1
        elif self.direction == "west":
            self.x -= 1

        # Give move command
        return {
            "task": "move",
            "parameters": self.direction
        }

# Depreciated
class test6:
    def __init__(self):
        self.coordinates = [0, 0]
        self.target = [-4, 6]

#    def run(self, taskResponse):
#        direction = moveTo(self.coordinates[0], self.coordinates[1], self.target[0], self.target[1])
#        adjustCoords(self.coordinates, direction)

#        if not direction == None:
#            return {
#                "task": "move",
#                "parameters": direction
#            }

class test7:
    def __init__(self, direction=None):
        if direction == None:
            self.direction = random.choice(("north", "east", "south", "west"))
        else:
            self.direction = direction
    
    def run(self, taskResponse):
        if taskResponse == False:
            self.direction = random.choice(("north", "east", "south", "west"))

        return {
            "task": "move",
            "parameters": self.direction
        }

class scanTest:
    def __init__(self, direction):
        self.direction = direction
    
    def run(self, taskResponse):
        # print taskResponse
        if not taskResponse == None:
            b = utilities.Board("BLANK")

            for i in taskResponse.keys():
                for j in taskResponse[i].keys():
                    for k in taskResponse[i][j].keys():
                        b.setTile(i, j, taskResponse[i][j][k], k)

            print()
            print(b)
            input()

        return {
            "task": "scan",
            "parameters": self.direction
        }

class digTest:
    def __init__(self):
        self.tick = 0
        self.x = 0
        self.y = 0
        
        self.position = 0
    
    def run(self, taskResponse):
        pass
