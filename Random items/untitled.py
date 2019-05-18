# import pygame
import sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary1 import *

def calcVelocity(direction, vel=1.0):
	velocity = Point(0,0)
	if direction == 0:#north
		velocity.y = -vel
	elif direction == 2:#east
		velocity.x = vel
	elif direction == 4:#south
		velocity.y = vel
	elif direction == 6:#west
		velocity.x = -vel
	return velocity

def reverseDirections(sprite):
	if sprite.direction == 0:
		sprite.direction = 4
	elif sprite.direction == 2:
		sprite.direction = 6
	elif sprite.direction == 4:
		sprite.direction = 0
	elif sprite.direction == 6:
		sprite.direction = 2 

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)
        

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)
#def drawIt(sprite,surface):
  #      surface.blit(, (sprite._getx, sprite._gety))

def printText(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

def resetBullet():
    y = random.randint(250,350)
    arrow.position = 800,y

pygame.init()
font = pygame.font.Font(None,36)
timer = pygame.time.Clock()

velocity = 10

window_width=1500
window_height=900

animation_increment=10
clock_tick_rate=20

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("Test game PyInvaders")

#INitialising moving characters etc
playerGroup = pygame.sprite.Group()
player = MySprite()
player.load("spaceship.png",96,96,1)
player.position =100,100
player.direction = 4
playerGroup.add(player)

playerMoving = False

dead=False

clock = pygame.time.Clock()
background_image = pygame.image.load("hubbleImage.png").convert()

black=(0,0,0)
end_it=False
while (end_it==False):
    #window.fill(black)
    myfont=pygame.font.SysFont("Comic Sans", 40)
    nlabel=myfont.render("Welcome to the Start Screen", 1, (255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            end_it=True
    screen.blit(nlabel,(200,200))
    pygame.display.flip()

count = 0
screen.blit(background_image, [0, 0])
while(dead==False):


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
    ticks = pygame.time.get_ticks()
    count+=1

    print("I'm in the main loop at count",count)

    #pygame.display.update()

    keys = pygame.key.get_pressed()

    if keys[K_ESCAPE]:
    	pygame.display.quit()
    	pygame.quit()
    	sys.exit()
    elif keys[K_UP] or keys[K_w]:
    	player.X += velocity
    	playerMoving = True
    elif keys[K_RIGHT] or keys[K_d]:
    	player.Y += velocity
    	playerMoving = True
    elif keys[K_DOWN] or keys[K_s]:
    	player.X -=velocity
    	playerMoving = True
    elif keys[K_LEFT] or keys[K_a]:
    	player.Y -= velocity
    	playerMoving = True
    else:
    	playerMoving = False

    playerGroup.update(ticks,50)

    #screen.blit(background_image, [0, 0])

    #if not dead:
    	#playerGroup.update(ticks,10)
    #playerGroup.draw(screen)



    

    pygame.display.flip()
    clock.tick(clock_tick_rate)
