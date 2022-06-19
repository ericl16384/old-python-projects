# Imports

# Standard imports
import importlib
import random
import os


# Globals
global cardinalDirs
cardinalDirs = ("north", "east", "south", "west")


# Functions

# No idea on credit for clearScreen()
def clearScreen():
    """Clears the screen"""
    if os.name == "nt": os.system("cls")
    else: os.system("clear")
clearScreen()

class SpeedList(list):
    """A type of list that is optimized for deleting entries. (Indexes never need to shift, but consumes more memory.)"""
    def __init__(self, arguments=[]):
        self.data = {}
        self.write = 0

        for arg in arguments:
            self.append(arg)
    
    def __getitem__(self, key):
        if key < 0 and key*-1 <= self.write:
            return self.data[self.write+key]
        elif key in self.data.keys():
            return self.data[key]
        else:
            raise IndexError
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __iter__(self):
        return iter([self.data[i] for i in self.data.keys()])
    
    def __len__(self):
        return self.write
    
    def __str__(self):
        return str(self.data)
    
    def append(self, argument):
        self.data[self.write] = argument
        self.write += 1

def getModule(codeModule, codePackage):
    """Warning: Returns the package, not an instance"""
    return getattr(importlib.import_module(codeModule), codePackage)


# Tiles

class Tile:
    def __init__(self, tileType, data={}):
        self.tileType = tileType
        self.data = {}
    
    def get(self):
        return self.tileType
    
    def getData(self):
        return self.data
    
    def setData(self, content):
        self.data = content

global tileTypes
tileTypes = ["grass", "stone", "ore"]


# Objects

class Object:
    def __init__(self, objectType, data={}):
        self.tileType = objectType
        self.data = {}
    
    def get(self):
        return self.tileType
    
    def getData(self):
        return self.data

class Entity(Object):
    def __init__(self, entityNumber, program):
        self.entityNumber = entityNumber
        self.program = program

        self.task = None
        self.taskResponse = None
    
    def getEntityNumber(self):
        return self.entityNumber
    
    def setTask(self, task):
        self.task = task

    def getTask(self):
        if self.task == None:
            return None
        else:
            return self.task["task"], self.task["parameters"]

    def setTaskResponse(self, response):
        self.taskResponse = response
    
    def getTaskResponse(self):
        return self.taskResponse

    def tick(self, board):
        # Do correct number of lines of code (currently all)
        self.setTask(self.program.run(self.getTaskResponse()))
    
        # Return command
        out = self.getTask()
        self.setTask(None)
        return out

class Robot(Entity):
    def __init__(self, entityNumber, program):
        self.entityNumber = entityNumber
        self.program = program

        self.task = None
        self.taskResponse = None

        self.scanPower = 3
        self.inventory = None
    
    def getScanPower(self):
        return self.scanPower
    
    def setScanPower(self, scanPower):
        self.scanPower = scanPower
        


# Board
class Board:
    def __init__(self, seed=None):
        if seed == None:
            random.seed()
            self.seed = random.randint(1, 2**64)
        else:
            self.seed = seed

        self.map = {}
        self.entities = SpeedList()
        self.tickNumber = 0
    
    def getSeed(self):
        return self.seed

    def setTile(self, x, y, content, level, autoGenerate=True):
        """Warning: disabling autoGenerate may result in errors"""

        if autoGenerate and x not in self.map.keys() or y not in self.map[x].keys():
            self.generateTile(x, y)

        self.map[x][y][level] = content

    def generateTile(self, x, y, level=None, force=False):
        if x not in self.map.keys():
            self.map[x] = {}
        if y not in self.map[x].keys():
            self.map[x][y] = {}

        if level == None or level == 0 and 0 not in self.map[x][y].keys or force:
            # Check for special seeds

            if self.getSeed() == "BLANK":
                tile = None
            
            # Seed is generic
            else:
                random.seed(str(self.getSeed())+str([x, y])+"0")
                tile = Tile(random.choice(tileTypes))

                if tile.get() == "ore":
                    random.seed(str(self.seed)+str([x, y])+"ore")
                    tile.setData({
                        "quantity": random.randint(10, 20)
                    })


            self.setTile(x, y, tile, 0, False)

        if level == None or level == 1 and 1 not in self.map[x][y].keys or force:
            # Check for special seeds

            if self.getSeed() == "BLANK":
                tile = None
            
            # Seed is generic
            else:
                #random.seed(str(self.getSeed())+str([x, y])+"1")

                tile = None

            self.setTile(x, y, tile, 1, False)

    def getTile(self, x, y, level=None):
        if x not in self.map.keys() or y not in self.map[x].keys():
            self.generateTile(x, y)

        if level == None:
            return self.map[x][y]
        else:
            return self.map[x][y][level]
    
    def copyTile(self, x1, y1, x2, y2, level):
        tile = self.getTile(x1, y1, level)
        self.setTile(x2, y2, tile, level)

        if issubclass(tile.__class__, Entity):
            self.entities[tile.getEntityNumber()][1] = x2
            self.entities[tile.getEntityNumber()][2] = y2

    def moveTile(self, x1, y1, x2, y2, level):
        self.copyTile(x1, y1, x2, y2, level)

        if not x1 == x2 or not y1 == y2:
            self.setTile(x1, y1, None, level)
    
    def shiftObject(self, x1, y1, direction, force=False):
        # Set target
        if direction == "north":
            x2 = x1
            y2 = y1+1
        elif direction == "south":
            x2 = x1
            y2 = y1-1
        elif direction == "east":
            x2 = x1+1
            y2 = y1
        elif direction == "west":
            x2 = x1-1
            y2 = y1
        else:
            raise AssertionError

        # Determine if possible
        if self.getTile(x2, y2, 1) == None or force:
            # success
            self.moveTile(x1, y1, x2, y2, 1)

            return True
        else:
            # failure
            return False
    
    def scan(self, x, y, direction, power):
        # Define area
        area = {
            0: {
                0: None
            }
        }


        # Add to area

        if direction == "north":
            for j in range(1, power+1):
                for i in range(j*-1, j+1):
                    if i not in area.keys():
                        area[i] = {}
                    if j not in area[i].keys():
                        area[i][j] = None
        elif direction == "south":
            for j in range(1, power+1):
                for i in range(j*-1, j+1):
                    if i not in area.keys():
                        area[i] = {}
                    if j not in area[i].keys():
                        area[i][j*-1] = None

        elif direction == "east":
            for i in range(1, power+1):
                for j in range(i*-1, i+1):
                    if i not in area.keys():
                        area[i] = {}
                    if j not in area[i].keys():
                        area[i][j] = None
        elif direction == "west":
            for i in range(1, power+1):
                for j in range(i*-1, i+1):
                    if i*-1 not in area.keys():
                        area[i*-1] = {}
                    if j not in area[i*-1].keys():
                        area[i*-1][j] = None

        else:
            raise AssertionError
        

        # Replace each blank in area with a tile
        for i in area.keys():
            for j in area[i].keys():
                area[i][j] = self.getTile(i+x, j+y)

                # Decending in priortity
                for k in area[i][j].keys():
                    if issubclass(area[i][j][k].__class__, Entity):
                        area[i][j][k] = area[i][j][k]

                    elif issubclass(area[i][j][k].__class__, (Tile, Object)):
                        area[i][j][k] = area[i][j][k]
        
        
        # Return
        return area
    
    def dig(self, x, y):
        tile = self.getTile(x, y, 0)

        if isinstance(tile, Tile) and tile.get() == "ore":
            data = tile.getData()
            data["quantity"] -= 1
            tile.setData(data)
            return True
        else:
            return False

    def addObject(self, x, y, name="", force=False):
        if self.getTile(x, y, 1) == None or force:
            self.setTile(x, y, Object(name), 1)
        
            return True
        else:
            return False
    
    def addEntity(self, x, y, program, force=False):
        if self.getTile(x, y, 1) == None or force:
            self.entities.append([Entity(len(self.entities), program), x, y])
            self.setTile(x, y, self.entities[-1][0], 1)
        
            return True
        else:
            return False
    
    def addRobot(self, x, y, program, force=False):
        if self.getTile(x, y, 1) == None or force:
            self.entities.append([Robot(len(self.entities), program), x, y])
            self.setTile(x, y, self.entities[-1][0], 1)
        
            return True
        else:
            return False

    def getTickNumber(self):
        return self.tickNumber

    def tick(self):
        self.tickNumber += 1

        for entity in self.entities:
            response = entity[0].tick(self)

            if response == None:
                continue

            # Entities
            elif response[0] == "move":
                entity[0].setTaskResponse(self.shiftObject(entity[1], entity[2], response[1]))
            
            # Robots
            elif response[0] == "scan":
                if issubclass(entity[0].__class__, Robot):
                    power = entity[0].getScanPower()

                    entity[0].setTaskResponse(self.scan(entity[1], entity[2], response[1], power))
                
                else:
                    raise AssertionError

            else:
                raise AssertionError

    def __str__(self):
        radius = 15 # min 0, but 10 works best
        center = [0, 0]
        edge = "█"
        doEdge = False

        out = ""

        if doEdge:
            out += edge*(radius*4+6)+"\n"

        for y in range(radius, radius*-1-1, -1):
            if doEdge:
                out += edge*2

            for x in range(radius*-1, radius+1):
                tile = self.getTile(x+center[0], y+center[1])

                # Decending by priortity
                
                # Level 1
        
                # Robot
                if issubclass(tile[1].__class__, Robot):
                    out += "R "

                # Entity
                elif issubclass(tile[1].__class__, Entity):
                    out += "E "
                
                # Object
                elif issubclass(tile[1].__class__, Object):
                    out += "O "
                
                # Level 0
                
                # Grass
                elif issubclass(tile[0].__class__, Tile) and tile[0].get() == "grass":
                    out += "//"
                
                # Stone
                elif issubclass(tile[0].__class__, Tile) and tile[0].get() == "stone":
                    out += "▒▒"
                
                # Ore
                elif issubclass(tile[0].__class__, Tile) and tile[0].get() == "ore":
                    out += "░░"

                # Anything else
                else:
                    out += "? "

            if doEdge:
                out += edge*2
            out += "\n"

        if doEdge:
            out += edge*(radius*4+6)

        return out
