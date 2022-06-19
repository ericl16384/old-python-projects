import technology

class Component:
    def __init__(self, name, tech, ironium, boranium, germanium, resources, mass):
        self.name = name
        self.tech = tech
        self.ironium = ironium
        self.boranium = boranium
        self.germanium = germanium
        self.resources = resources
        self.mass = mass

    def getName(self):
        return self.name
    def getTech(self):
        return self.tech
    def getIronium(self):
        return self.ironium
    def getBoranium(self):
        return self.boranium
    def getGermanium(self):
        return self.germanium
    def getResources(self):
        return self.resources
    def getMass(self):
        return self.mass

class Engine(Component):
    def __init__(self, name, tech, ironium, boranium, germanium, resources, mass, warp, safe):
        super().__init__(name, tech, ironium, boranium, germanium, resources, mass)

        self.warp = warp
        self.safe = safe

class Scanner(Component):
    def __init__(self, name, tech, ironium, boranium, germanium, resources, mass, range, advRange):
        super().__init__(name, tech, ironium, boranium, germanium, resources, mass)
        
        self.range = range
        self.advRange = advRange

components = [
    Engine("Long Hump 6", technology.Tech(pr=3), 3, 0, 1, 4, 9, [None, 0, 0.25, 0.5, 1, 1, 1, 4, 6, 8, 8], 9),
    Scanner("Bat Scanner", technology.Tech(), 1, 0, 1, 1, 2, 0, 0)
]

def index(i):
    return components[i]
