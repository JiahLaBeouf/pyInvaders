#functions.py
import pygame
from pygame.locals import *

def clearScreenBG(s,bg):
	s.fill((0,0,0))
	s.blit(bg,(0,0))
	pygame.display.flip()