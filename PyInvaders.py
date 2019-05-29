#PyInvaders.py (essentially the main file)

import lib
from lib import *

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

#call the "main" function if running this script

#Welcome to PyInvaders version 1.2

main()
