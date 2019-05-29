#functions.py
import pygame
from pygame.locals import *
import random,os

#Clears the screen by filling with the background image supplied
def clearScreenBG(s,bg):
	s.fill((0,0,0))
	s.blit(bg,(0,0))
	pygame.display.flip()

mainDir = os.path.split(os.path.abspath(__file__))[0]

#This function loads an image from the data folder in the classpath, returns as a converted image
def loadImage(file):
    "loads an image, prepares it for play"
    file = os.path.join(mainDir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

#This function loads multiple images from the data folder and returns them as an array of images
def loadImages(*files):
    imgs = []
    for file in files:
        imgs.append(loadImage(file))
    return imgs


#Prints the wanted text in the centre of the screen, takes the y, message, the screen to place on and the colour
def printCText(y, text,screen,colour):
    font = pygame.font.Font("data/VT323-Regular.ttf", 50)
    imgText = font.render(text, True,colour)
    x = (800 - imgText.get_width())/2
    screen.blit(imgText, (x,y))
    pygame.display.update()

#Prints text at any size and places in the centre of the screen at any y, screen and colour
def printSCText(y, text,screen,colour,size):
    font = pygame.font.Font("data/VT323-Regular.ttf", size)
    imgText = font.render(text, True,colour)
    x = (800 - imgText.get_width())/2
    screen.blit(imgText, (x,y))
    pygame.display.update()

#Prints text at a given x,y coordinate and takes a colour as well as the message and screen
def printText(x,y, text,screen,colour):
    font = pygame.font.Font("data/VT323-Regular.ttf", 50)
    imgText = font.render(text, True,colour)
    #x = (800 - imgText.get_width())/2
    screen.blit(imgText, (x,y))
    pygame.display.update()

#Places a given image at the specified xy coordinate of given screen
#Returns the image as a converted object
def placeImage(image,x,y,screen):
	img = loadImage(image)
	screen.blit(img , (x,y))
	pygame.display.update() # paint screen one time
	return img

#places an image at the centre of a given y value on given screen
#Returns the image as a converted object
def placeCImage(image,y,screen):
	img = loadImage(image)
	x = (800-img.get_width())/2
	screen.blit(img,(x,y))
	pygame.display.update()
	return img

#Tests the sound system
class dummysound:
    def play(self): pass

#Loads a sound from the data folder
def loadSound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(mainDir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

#Self made collide point object, checks if an xy input is within the rectangle of an object.
def collideP(xO,yO,object, x,y):
	if xO<=x<=(xO+object.get_width()) and yO<=y<=(yO+object.get_height()):
		return True

