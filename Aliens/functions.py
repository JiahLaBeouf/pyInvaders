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

def printCText(y, text,screen,colour):
    font = pygame.font.Font("data/VT323-Regular.ttf", 50)
    imgText = font.render(text, True,colour)
    x = (800 - imgText.get_width())/2
    screen.blit(imgText, (x,y))
    pygame.display.update()

def printSCText(y, text,screen,colour,size):
    font = pygame.font.Font("data/VT323-Regular.ttf", size)
    imgText = font.render(text, True,colour)
    x = (800 - imgText.get_width())/2
    screen.blit(imgText, (x,y))
    pygame.display.update()

def printText(x,y, text,screen,colour):
    font = pygame.font.Font("data/VT323-Regular.ttf", 50)
    imgText = font.render(text, True,colour)
    #x = (800 - imgText.get_width())/2
    screen.blit(imgText, (x,y))
    pygame.display.update()

def placeImage(image,x,y,screen):
	img = load_image(image)
	screen.blit(img , (x,y))
	pygame.display.update() # paint screen one time
	return img

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

def collideP(xO,yO,object, x,y):
	if xO<=x<=(xO+object.get_width()) and yO<=y<=(yO+object.get_height()):
		return True

