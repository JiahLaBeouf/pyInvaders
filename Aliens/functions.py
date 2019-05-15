#functions.py
import pygame
from pygame.locals import *
import random,os

def clearScreenBG(s,bg):
	s.fill((0,0,0))
	s.blit(bg,(0,0))
	pygame.display.flip()

main_dir = os.path.split(os.path.abspath(__file__))[0]

#This function loads an image from the data folder in the classpath
def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

#This function loads multiple images from the data folder
def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

def printText(x, y, text,screen):
    font = pygame.font.Font(None, 50)
    imgText = font.render(text, True, (255,255,255))
    screen.blit(imgText, (x,y))

class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()