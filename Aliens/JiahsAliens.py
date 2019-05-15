#JiahsAliens.py (essentially the main file)

import lib
from lib import *

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

#call the "main" function if running this script

main()

# Some To Dos:
#     Make sure to create the startup menu, to do a few things:
#         1. pick which ship the player wants to play with (which inevitably starts the game)
#         2. has a credits section
#         3. leaderboard?
#     End game section:
#         1. links back to start menu or
#         2. has an exit button which exits the game

# Tasks for 15/05:
#     new graphics for all buttons
#     populate menus (starting + ending)
#     new graphics for aliens, bullets, bombs, homebase
#     create a health powerup? (basically copy bombs but for different purposes)
#     create installation guide and user manual
#     create survey
