import random

import utilities

class Elliott_Robot():
    def __init__(self, directions=["north", "east", "south", "west"]):
        self.directions = directions
        self.opposites = {"north" : "south", "east" : "west", "south" : "north", "west" : "east"}
        self.dictator = 1
    
    def run(self, taskResponse):
        self.direction = random.choice(self.directions)
        if self.dictator >= 0:
            self.directions.append(self.opposites[self.direction])
        else:
            self.directions.remove(self.direction)
        
        self.dictator = random.randint(-4, 8)
        return {
            "task": "move",
            "parameters": self.direction
        }