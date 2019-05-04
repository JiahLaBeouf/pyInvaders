#Testing the moving character

#import statements
import sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary1 import *

pygame.init()
font = pygame.font.Font(None,36)
timer = pygame.time.Clock()

window_width=1500
window_height=900

animation_increment=10
clock_tick_rate=20

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("Test game PyInvaders")