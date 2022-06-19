# Switching between users
user = "Eric"


# Imports

# Standard imports
import random
import time

# Custom imports
import utilities



# Stimuli

board = utilities.Board()
program = ""


# Eric's testing
if user == "Eric":
    #program = "digTest"
    program = "scanTest"

    board.addRobot(0, 0, utilities.getModule("programs.eric", program)("north"))

# Elliott's challenge
elif user == "Elliott":
    program = "Elliott_Robot"

    robotLocations = (
        (0, 0),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1)
    )

    for i in robotLocations:
        board.addRobot(i[0], i[1], utilities.getModule("programs.elliott", program)())


    # Add wall
    difficulty = 4
    for i in range(-8, 9):
        # North
        if random.randint(0, difficulty) > 0:
            board.addObject(i, 9)
    
        # South
        if random.randint(0, difficulty) > 0:
            board.addObject(i, -9)

        # East
        if random.randint(0, difficulty) > 0:
            board.addObject(9, i)

        if random.randint(0, difficulty) > 0:
            board.addObject(-9, i)

# Russ' challenge
elif user == "Russ":
    program = "Russ_Mapper"

    robotLocations = (
        (0, 0),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1)
    )

    for i in robotLocations:
        board.addRobot(i[0], i[1], utilities.getModule("programs.russ", program)())


    # Add wall
    difficulty = 20
    for i in range(-12, 13):
        # North
        if random.randint(0, difficulty) > 0:
            board.addObject(i, 13)
    
        # South
        if random.randint(0, difficulty) > 0:
            board.addObject(i, -13)

        # East
        if random.randint(0, difficulty) > 0:
            board.addObject(13, i)

        if random.randint(0, difficulty) > 0:
            board.addObject(-13, i)

else:
    raise AssertionError("user is not valid")



# Response

printed = str(board)
auto = 0

while True:
    # Board
    print(printed)
    print()

    # Footer
    print(f"SEED = {board.getSeed()}")
    print(f"PROGRAM = \"{program}\"")
    print(f"TIME = {board.getTickNumber()}")
    print()

    if not auto == 0:
        print("AUTO MODE ACTIVATED")

        if auto > 0:
            print(f"DEACTIVATING IN {auto}")
            auto -= 1

        time.sleep(0.5)
    else:
        print("PRESS ENTER TO TO INCREMENT FORWARD")
        print("TYPE \"AUTO\" TO INCREMENT FORWARD INDEFINITELY")
        print("TYPE \"AUTO [X]\" TO INCREMENT FORWARD X STEPS")
        print()
        ans = input(">>> ")

        if ans[:4].lower() == "auto":
            if len(ans) == 4:
                auto = -1
            else:
                try:
                    auto = int(ans[5:])-1
                except:
                    pass

    # Increment state
    board.tick()
    printed = str(board)

    # Prepare to draw
    utilities.clearScreen()
