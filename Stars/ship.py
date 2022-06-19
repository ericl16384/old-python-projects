from components import index as components
import technology

class Ship:
    def __init__(self, name, hull, slots):
        assert isinstance(name, str)
        assert isinstance(hull, str)
        assert isinstance(slots, list)

        assert hull in hulls
        assert len(slots) == len(hulls[hull]["slots"])

        self.tech = hulls[hull]["tech"]
        self.ironium = hulls[hull]["ironium"]
        self.boranium = hulls[hull]["boranium"]
        self.germanium = hulls[hull]["germanium"]
        self.resources = hulls[hull]["resources"]
        self.mass = hulls[hull]["mass"]

        self.fuel = hulls[hull]["fuel"]
        self.armor = hulls[hull]["armor"]
        self.initiative = hulls[hull]["initiative"]

        for component, slot in zip(slots, hulls[hull]["slots"]):
            if component == None:
                continue
            
            assert isinstance(component, list)
            assert isinstance(slot, list)

            assert len(component) == 2
            assert len(slot) == 4 

            assert components(component[0]).__class__.__name__ == slot[0]

            assert component[1] <= slot[1]

            self.tech += components(component[0]).getTech()
            self.ironium += components(component[0]).getIronium()

        self.name = name
        self.hull = hull

        self.slots = slots

    def __str__(self):
        return """
"""

    def getTech(self):
        return self.tech
    def getIronium(self):
        return self.ironium

# [type, quantity, x, y]
hulls = {
    "Scout": {
        "tech": technology.Tech(),
        "ironium": 3,
        "boranium": 2,
        "germanium": 3,
        "resources": 8,
        "mass": 8,

        "fuel": 50,
        "armor": 20,
        "initiative": 1,

        "slots": [
            ["Engine", 1, 0, 0],
            ["General Purpose", 1, 1, 0],
            ["Scanner", 1, 2, 0]
        ]
    }
}
