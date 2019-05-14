#The location of all the classes and functions

#additional import statements necessary for the program
import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

#Game constants, used mostly in the main subprogram
MAX_SHOTS      = 4      #most player bullets onscreen
ALIEN_ODDS     = 10     #chances a new alien appears
BOMB_ODDS      = 20    #chances a new bomb will drop
ALIEN_RELOAD   = 6     #frames between new aliens
SCREENRECT     = Rect(0, 0, 700, 480)
SCORE          = 0
LIVES = 3

#This directs the program to understand where to look for additional files
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

def printText(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
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



# each type of game object gets an init and an
# update function. the update function is called
# once per frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about
# the keyboard


class Player(pygame.sprite.Sprite):
    speed = 10
    bounce = 24
    gun_offset = 0
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1,1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
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
    speed = -13
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
        self.rect = self.image.get_rect(midbottom=
                    alien.rect.move(0,5).midbottom)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 470:
            Explosion(self)
            self.kill()


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 30)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)

class Lives(pygame.sprite.Sprite):
    #LIFE = 3
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 30)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastlife = 4
        self.update()
        #print("lives update called")
        self.rect = self.image.get_rect().move(10, 420)

    def update(self):
        if LIVES != self.lastlife:
            self.lastlife = LIVES
            msg2 = "Lives Remaining: %d" % LIVES
            self.image = self.font.render(msg2, 0, self.color)
            #print("in lives update")

class Title(pygame.sprite.Sprite):
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(350,400)

class SelectableShip(pygame.sprite.Sprite):
    images=[]
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        










def main(winstyle = 0):
    # Initialize pygame
    if pygame.get_sdl_version()[0] == 2:
        pygame.mixer.pre_init(44100, 32, 2, 1024)
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #This should be where the start menu goes


    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    img = load_image('ship.gif')
    Player.images = [img, pygame.transform.flip(img, 1, 0)]
    img = load_image('explosion1.gif')
    Explosion.images = [img, pygame.transform.flip(img, 1, 1)]
    Alien.images = load_images('alien1.gif', 'alien2.gif', 'alien3.gif')
    Bomb.images = [load_image('bomb.gif')]
    Shot.images = [load_image('bullet.jpg')]
    img = load_image('player1.gif')
    HomeBase.images = [img,pygame.transform.flip(img,1,0)]
    print("HomeBase image loaded")

    #decorate the game window
    icon = pygame.transform.scale(Alien.images[0], (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Jiah Presents: Aliens')
    pygame.mouse.set_visible(0)

    #create the background, tile the bgd image
    bgdtile = load_image('hubbleimage.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #load the sound effects
    boom_sound = load_sound('boom.wav')
    shoot_sound = load_sound('car_door.wav')
    if pygame.mixer:
        music = os.path.join(main_dir, 'data', 'house_lo.wav')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    # Initialize Game Groups
    aliens = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    #homeBase = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    lastalien = pygame.sprite.GroupSingle()

    #assign default groups to each sprite class
    Player.containers = all
    Alien.containers = aliens, all, lastalien
    HomeBase.containers = all
    Shot.containers = shots, all
    Bomb.containers = bombs, all
    Explosion.containers = all
    Score.containers = all
    Lives.containers = all
    

    #Create Some Starting Values
    global score
    global lives
    alienreload = ALIEN_RELOAD
    kills = 0
    clock = pygame.time.Clock()

   #homeBase.position = 300,300
    #print("homebase position called ")

    #initialize our starting sprites
    global SCORE
    global LIVES
    player = Player()
    Alien() #note, this 'lives' because it goes into a sprite group
    if pygame.font:
        all.add(Score())
        all.add(Lives())

    homeBase = HomeBase()
    print("homeBase=HomeBase()")

    #more self additions, the maxshots is for creating an increasing amount of bullets on the screen proportional to the score
    maxShots = 4
    #the amount of lives a player begins with, the lives can only  be diminished by bombs, if an alien comes into contact then it is game over.
    lives = 3
    #LIVES = lives

    while player.alive():
        LIVES = lives

        #get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            elif event.type == KEYDOWN:
                if event.key == pygame.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pygame.display.set_mode(
                            SCREENRECT.size,
                            winstyle | FULLSCREEN,
                            bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pygame.display.set_mode(
                            SCREENRECT.size,
                            winstyle,
                            bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    # screen.fill((255, 0, 0))
                    pygame.display.flip()
                    fullscreen = not fullscreen


        keystate = pygame.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        #update all the sprites
        all.update()
        homeBase.update()

        
        #handle player input
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction)
        direction2 = keystate[K_UP] - keystate[K_DOWN]
        homeBase.move(direction2)
        firing = keystate[K_SPACE]
        if not player.reloading and firing and len(shots) < maxShots:
            Shot(player.gunpos())
            shoot_sound.play()
        player.reloading = firing

        # Create new alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            Alien()
            alienreload = ALIEN_RELOAD
        # Drop bombs
        if lastalien and not int(random.random() * BOMB_ODDS):
            Bomb(lastalien.sprite)

        # Detect collisions
        for alien in pygame.sprite.spritecollide(player, aliens, 1):
            boom_sound.play()
            Explosion(alien)
            Explosion(player)
            SCORE = SCORE + 1
            player.kill()

        for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
            boom_sound.play()
            Bomb(alien)
            Explosion(alien)
            SCORE = SCORE + 1

        for bomb in pygame.sprite.spritecollide(player, bombs, 1):
            boom_sound.play()
            Explosion(player)
            Explosion(bomb)
            #player.kill()
            lives-=1

        for bomb in pygame.sprite.spritecollide(homeBase, bombs, 1):
            boom_sound.play()
            Explosion(homeBase)
            Explosion(bomb)
            print("Homebase was hit")
            player.kill()

            #introduction of lives into the game

            #ToDo: Create a loseLife method which also shows remaining lives on the screen
            lives-=1

        #Creation of this is to introduce new scoring methods, shooting a bomb is worth double points
        for shot in pygame.sprite.groupcollide(bombs, shots, 1, 1).keys():
            boom_sound.play()
            Explosion(shot)
            #Explosion(bomb)
            #player.kill()
            
            #Bonuses for shooting a bomb
            SCORE = SCORE + 2
            #Potential powerup for every bomb scored? or possibly for the actual score count.


        if lives==0:
            player.kill()

            #The old formula for how many shots, however we may limit this to max 8
        # if SCORE>=10:
        #     maxShots = round(SCORE*0.1) + 4
        # else:
        #     maxShots = 4
        # #print(maxShots)


        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(40)

    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)
    pygame.quit()

