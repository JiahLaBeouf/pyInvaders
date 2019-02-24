#MyLibrary.py

import sys,time,random,math,pygame
from pygame import *

def printText(font,x,y,text,color=(255,255,255)):
	imgText = font.render(text, True, color)
	screen = pygame.display.get_surface()
	screen.blit(imgText,(x,y))

class MySprite(pygame.sprite.Sprite):

	#init method
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #extends base class
		self.masterImage = None
		self.frame = 0
		self.oldFrame = -1
		self.frameWidth = 1
		self.frameHeight = 1
		self.firstFrame = 0
		self.lastFrame = 0
		self.columns = 12
		self.lastTime = 0
		self.direction = 0
		self.velocity = Point(0.0,0.0)

	#x property
	def _getx(self):
		return self.rect.x
	def _setx(self,value):
		self.rect.x = value
	X = property(_getx,_setx)

	#y property
	def _gety(self):
		return self.rect.y
	def _sety(self,value):
		self.rect.y = value
	Y = property(_gety,_sety)

	#position
	def _getpos(self):
		return self.rect.topleft
	def _setpos(self,pos):
		self.rect.topleft = pos
	position = property(_getpos,_setpos)

	#load
	def load(self, filename, width, height, columns):
		self.masterImage = pygame.image.load(filename).convert_alpha()
		self.frameWidth = width
		self.frameHeight = height
		self.rect = Rect(0,0,width,height)
		self.columns = columns

		#calculate total frames
		rect = self.masterImage.get_rect()
		self.lastFrame = (rect.width // width) * (rect.height // height) - 1

	def update(self,currentTime,rate=30):

		if currentTime > self.lastTime + rate:
			self.frame += 1
			if self.frame > self.lastFrame:
				self.frame = self.firstFrame
			self.lastTime = currentTime

		if self.frame != self.oldFrame:
			frameX = (self.frame % self.columns)*self.frameWidth
			frameY = (self.frame // self.columns)*self.frameHeight
			rect = Rect(frameX,frameY, self.frameWidth,self.frameHeight)
			self.image = self.masterImage.surface(rect)
			self.oldFrame = self.frame

	def __str__(self):
		return str(self.frame)+","+str(self.firstFrame)+","+str(self.lastFrame)+","+str(self.frameWidth)+","+str(self.frameHeight)+","+str(self.columns)+","+str(self.rect)

class Point(object):

	def __init__(self,x,y):
		self.__x = x
		self.__y = y

	#X
	def getx(self):
		return self.__x
	def setx(self,x):
		self.__x = x
	x = property(getx,setx)

	#Y
	def gety(self):
		return self.__y
	def sety(self,y):
		self.__y = y
	y = property(gety,sety)

	def __str__(self):
		return "{X:"+"{:.0f}".format(self.__x)+",Y:"+"{:.0f}".format(self.__y)+"}"

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

