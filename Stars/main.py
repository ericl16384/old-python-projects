import components
import planet
import ship
import starbase
import technology
import turn

def main():
    shipBlueprints = []
    starbaseBlueprints = []

    shipBlueprints.append(ship.Ship("Probe", "Scout", [[0, 1], None, [1, 1]]))

##    print(shipBlueprints[0].getTech())
##    print()
##    print(shipBlueprints[0].getIronium())
    print(shipBlueprints[0])



if __name__ == "__main__":
    main()
