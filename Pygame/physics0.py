"1/9/2021"


# Imports

import sys, os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.version import ver
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

class PhysicsObject:
    def __init__(self, vertices: Matrix, position=Vector(), rotation=0, velocity=Vector(), rotationSpeed=0, centerOfMass=None, mass=1, image=None):
        self.vertices = vertices.resize(height=2)

        self.position = position.resize(2)
        self.velocity = velocity.resize(2)

        self.rotation = rotation
        self.rotationSpeed = rotationSpeed

        self.mass = mass

        if image:
            self.image = image
            self.imageIsTemporary = False
        else:
            self.imageIsTemporary = True

        self.init(centerOfMass)
    def init(self, centerOfMass=None):
        "Call this after changing vertices"

        # Resize
        self.vertices.resize(height=2)

        # Set up the center of mass
        if not centerOfMass:
            # Average of vertices
            centerOfMass = self.vertices.sum()/len(self.vertices)
        
        # Move origin to center of mass
        self.vertices = self.vertices.offset(-centerOfMass)

        # Construct image if neccessary
        if self.imageIsTemporary:
            bounds = self.vertices.bounds()
            self.image = pygame.Surface(bounds.sum())
            self.image.set_colorkey(BLACK)
            pygame.draw.polygon(self.image, WHITE, self.vertices.offset(-bounds[0]))


    def applyForce(self, vector):
        "Applies at center of mass" # Cannot induce rotation
        
        self.velocity += vector/self.mass
    def applyForceAtLocation(self, vector, location):
        raise NotImplementedError
    
    def getTransformed(self):
        return self.vertices.rotate(self.rotation).offset(self.position)
    def step(self):
        self.position += self.velocity
        self.rotation += self.rotationSpeed
    def draw(self, surface, cameraPos=Vector(), debug=False):
        vertices = self.getTransformed()

        # Attempts at rotating and bliting images

        # Will be replaced with an image
        #image = pygame.Surface(abs(bounds).sum())
        #image.set_colorkey(BLACK)
        #image.fill(BLACK)
        ##pygame.draw.polygon(image, WHITE, vertices.offset(-bounds[0]))
        #pygame.draw.polygon(image, WHITE, vertices.offset(Vector(image.get_width(), image.get_height())))
        #surface.blit(image, drawPos)

        ##image = pygame.transform.rotate(self.image, self.rotation)
        ##image = self.image
        #image = pygame.Surface(self.vertices.bounds().sum())
        #image.fill(WHITE)

        #print(self.position + Vector(*image.get_size())/2)
        #surface.blit(image, image.get_rect())
        ##surface.blit(image, self.position + Vector(*image.get_size())/2)


        # Draw ship

        pygame.draw.polygon(surface, WHITE, vertices.offset(-cameraPos))


        # Debug (do not antialiase, for speed)

        if debug:

            # Hitbox
            pygame.draw.polygon(surface, RED, vertices.offset(-cameraPos), 1)

            # Center of mass
            pygame.draw.circle(surface, RED, self.position-cameraPos, 1)


# Constants

# Max for my screen is 1366x768
# If is 0x0, it will default to the size of the screen (see next line)
# If is the size of the screen or larger it will be fullscreen
SCREEN_SIZE = Vector(0, 0)

# | is bitwise OR. Use it to combine flags
# Use 0 instead of None
#pygame.FULLSCREEN    create a fullscreen display (set SCREEN_SIZE to 0x0)
#pygame.DOUBLEBUF     recommended for HWSURFACE or OPENGL
#pygame.HWSURFACE     hardware accelerated, only in FULLSCREEN
#pygame.OPENGL        create an OpenGL-renderable display
#pygame.RESIZABLE     display window should be sizeable (pauses while resizing)
#pygame.NOFRAME       display window will have no border or controls
SCREEN_FLAGS = 0

TICKS_PER_SECOND = 60

#TICK_LENGTH = 1000/TICKS_PER_SECOND


# On not inported

def main():
    # Init

    # Objects
    print("Initializing objects.")
    ship = PhysicsObject(Matrix(
        #circlePos(0)*1.5,
        #circlePos(120),
        #circlePos(240)
        Vector(0, 0),
        Vector(1, 2),
        Vector(2, 0)
    )*20,
        velocity=Vector(2, 1), rotationSpeed=1
    )

    # Pygame
    print("Starting Pygame.")
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS)
    pygame.display.set_caption(os.path.basename(__file__))
    clock = pygame.time.Clock()


    # Main loop

    while True:
        # Draw

        # Cover up the previous stuff
        screen.fill(BLACK)

        # Draw poly ship
        ship.draw(screen, debug=True)

        # Show the screen (all screens?)
        pygame.display.flip()


        # Wait for the next tick

        clock.tick(TICKS_PER_SECOND)
        

        # Read input

        # Quit when exit button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endSimulation()

        
        # Physics TODO
            
        ship.step()


        ## Wait for the next tick
        #tickEnd = pygame.time.get_ticks()
        #pygame.time.wait(int(tickNext - tickEnd)) # Faster than .delay()

if __name__ == "__main__":
    main()
