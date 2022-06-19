# Imports

import os
from maths import *

try:
    import pygame
except ModuleNotFoundError:
    pygame = False


# Constants

# Colors
# Grayscale
WHITE  = 255, 255, 255
BLACK  =   0,   0,   0
GREY   = 128, 128, 128
# Primary
RED    = 255,   0,   0
GREEN  =   0, 255,   0
BLUE   =   0,   0, 255
# Secondary
YELLOW = 255, 255,   0
PURPLE = 255,   0, 255
CYAN   =   0, 255, 255
# Tertiary
# Quaternary
# Quinary
# Senary
# Septenary
# Octonary
# Nonary
# Denary


# Classes

#class Image(Matrix): # TODO
#    def getAntiAliased(self):
#        raise NotImplementedError


# Description

if __name__ == "__main__":
    print(f"{os.path.basename(__file__)} is a library in progress made by Eric Lewis.")
    input("Press ENTER for contents.")
    print()
    for k, v in globals().copy().items():
        if not k.startswith("__"):
            print(f"{k} = {v}")
