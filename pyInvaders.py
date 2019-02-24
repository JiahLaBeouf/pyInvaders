import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *

Background = Background('hubbleImage.png',(0,0))






pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("pyInvaders")
font = pygame.font.Font(None,36)
timer = pygame.time.Clock()


while True:
	#screen.fill([255, 255, 255])
	screen.blit(Background.image, Background.rect)
	