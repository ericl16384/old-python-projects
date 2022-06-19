"1/8/2021"


# Imports

import sys, os
import pygame
from graphics import *
from maths import *


# Functions

def endSimulation():
    if pygame.get_init():
        pygame.quit()
        print("Successfully exited Pygame.")

    print("Program end.")
    sys.exit()


# Classes

#class PygameSession: # Maybe TODO later
#    def __init__(self, tickFunction, surfaceSize, tickLength=100, caption="Pygame Session"):
#        self.tickFunction = tickFunction
#        self.surfaceSize = surfaceSize
#        self.tickLength = tickLength
#        self.caption = caption
    
#    def start(self):
#        while True:
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    # END LOOP
#                    # Maybe finalize a few things, like asking to save
#                    pygameLoopRunning = False
#                    continue


# Constants

SCREEN_SIZE = Vector(800, 450)
TICKS_PER_SECOND = 60
TICK_LENGTH = 1000/TICKS_PER_SECOND
PHYSICS_STEPS_PER_TICK = 10


# Pygame

# Startup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(os.path.basename(__file__))

# Construct ball
ballSize = Vector(*[10,]*2)
ball = pygame.Surface(ballSize.get())
ballRect = ball.get_rect()
ball.set_colorkey(BLACK)
ball.fill(BLACK)
pygame.draw.ellipse(ball, WHITE, ballRect)
ballTailLength = 1000

# Ball variables
ballPos = Vector(0, 0)
ballV = Vector(5, 1)

# Ball history
ballHistory = []

print("Successfully started Pygame.")

while True:
    # Work out when the next tick should be

    tickStart = pygame.time.get_ticks()
    tickNext = tickStart + TICK_LENGTH


    # Draw

    # Cover up the previous stuff
    screen.fill(GREY)

    # Draw the ball history
    whiteTail = ballHistory[:-ballTailLength]
    redTail = ballHistory[-ballTailLength-1:]
    # Efficent method for white lines
    if len(whiteTail) > 1:
        pygame.draw.aalines(screen, WHITE, False, whiteTail)
    # Less efficent for red gradient lines
    for i in range(len(redTail)-1):
        grade = (len(redTail)-1-i)/ballTailLength*255
        pygame.draw.aaline(screen, (grade, grade, grade), redTail[i], redTail[i+1])

    # Copy pixels from the ball to the screen, at the correct location
    screen.blit(ball, ballPos.get())

    # Show the screen (all screens?)
    pygame.display.flip()
    

    # Read input

    # Quit when exit button is clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endSimulation()


    # Physics TODO
    
    for i in range(PHYSICS_STEPS_PER_TICK):
        # Add velocity
        ballPos += ballV

        # X collisions
        if ballPos[0]+ballRect.left < 0:
            ballV[0] = abs(ballV[0])
        elif ballPos[0]+ballRect.right > SCREEN_SIZE[0]:
            ballV[0] = -abs(ballV[0])

        # Y collisions
        if ballPos[1]+ballRect.top < 0:
            ballV[1] = abs(ballV[1])
        elif ballPos[1]+ballRect.bottom > SCREEN_SIZE[1]:
            ballV[1] = -abs(ballV[1])
        
        # Update ball history
        ballHistory.append((ballPos+ballSize/2).get())


    # Wait for the next tick
    tickEnd = pygame.time.get_ticks()
    pygame.time.wait(int(tickNext - tickEnd)) # Faster than .delay()


print("Successfully exited Pygame.")
