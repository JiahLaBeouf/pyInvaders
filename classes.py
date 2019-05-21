#classes.py

import pygame
from pygame.locals import *
import random,os
import lib
from lib import *

class Player(pygame.sprite.Sprite):
    speed = 15
    bounce = 24
    gun_offset = 0
    images = []
    sr = None
    def __init__(self,scrt):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.sr = scrt
        self.rect = self.image.get_rect(midbottom=self.sr.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction,clockedSpeed):
        if direction: self.facing = direction
        self.rect.move_ip(direction*self.speed*clockedSpeed, 0)
        self.rect = self.rect.clamp(self.sr)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

    def gunpos(self):
        pos = self.facing*self.gun_offset + self.rect.centerx
        return pos, self.rect.top

class HomeBase(pygame.sprite.Sprite):
    speed = 0
    bounce = 24
    gun_offset = 0
    images = []
    sr = None
    def __init__(self,scrt):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.sr = scrt
        self.rect = self.image.get_rect(midbottom=self.sr.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(self.sr)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

    def gunpos(self):
        pos = self.facing*self.gun_offset + self.rect.centerx
        return pos, self.rect.top



class Alien(pygame.sprite.Sprite):
    speed = 13
    animcycle = 12
    images = []
    sr = None
    def __init__(self,scrt):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.sr = scrt
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1,1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = self.sr.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not self.sr.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(self.sr)
        self.frame = self.frame + 1
        self.image = self.images[self.frame//self.animcycle%3]
        #print("Alien Update called")


class Explosion(pygame.sprite.Sprite):
    defaultlife = 12
    animcycle = 3
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        self.life = self.life - 1
        self.image = self.images[self.life//self.animcycle%2]
        if self.life <= 0: self.kill()


class Shot(pygame.sprite.Sprite):
    speed = -15
    images = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    speed = 11
    images = []
    def __init__(self, alien):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=alien.rect.move(0,5).midbottom)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 540:
            Explosion(self)
            self.kill()

class Health(pygame.sprite.Sprite):
    speed = 13
    images = []
    def __init__(self, alien):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=alien.rect.move(0,5).midbottom)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 540:
            #Explosion(self)
            self.kill()

