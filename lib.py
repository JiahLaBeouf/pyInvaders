#The location of all the classes and functions

#additional import statements necessary for the program
import random, os.path, sys, webbrowser

import functions
from functions import *

import classes
from classes import *

#import basic pygame modules
import pygame
from pygame.locals import *

#Game constants, used mostly in the main subprogram
MAX_SHOTS      = 4      #most player bullets onscreen
ALIEN_ODDS     = 10     #chances a new alien appears
BOMB_ODDS      = 20    #chances a new bomb will drop
ALIEN_RELOAD   = 6     #frames between new aliens

class Score(pygame.sprite.Sprite):
    #score = None
    def __init__(self,score):
        pygame.sprite.Sprite.__init__(self)
        #self.score = score
        self.font = pygame.font.Font(None, 30)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        if score != self.lastscore:
            self.lastscore = score
            msg = "Score: %d" % score
            self.image = self.font.render(msg, 0, self.color)

class Lives(pygame.sprite.Sprite):
    #LIFE = 3
    #lf = None
    def __init__(self,lives):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 30)
        #self.lf = lives
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastlife = 4
        self.update()
        #print("lives update called")
        self.rect = self.image.get_rect().move(10, 420)

    def update(self):
        if lives != self.lastlife:
            self.lastlife = lives
            msg2 = "Lives Remaining: %d" % lives
            self.image = self.font.render(msg2, 0, self.color)
            #print("in lives update")

def main(winstyle = 0):
    # Initialize pygame
    if pygame.get_sdl_version()[0] == 2:
        pygame.mixer.pre_init(44100, 32, 2, 1024)
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    screenRect = Rect(0, 0, 800, 550)
    clock = pygame.time.Clock()
    dt = clock.tick(800)
    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(screenRect.size, winstyle, 32)
    screen = pygame.display.set_mode(screenRect.size, winstyle, bestdepth)
    white = (255,255,255)
    green = (23, 255, 15)
    

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    
    img = load_image('explosion1.gif')
    Explosion.images = [img, pygame.transform.flip(img, 1, 1)]
    Alien.images = load_images('alien1.gif', 'alien2.gif', 'alien3.gif')
    Bomb.images = [load_image('bomb.gif')]
    Shot.images = [load_image('shot.gif')]
    

    #SelectableShip.images = load_image("shipRainbow.gif")

    #decorate the game window
    icon = pygame.transform.scale(Alien.images[0], (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Jiah Presents: Aliens')
    

    #create the background, tile the bgd image
    bgdtile = load_image('hubbleimage.png')
    background = pygame.Surface(screenRect.size)
    for x in range(0, screenRect.width, bgdtile.get_width()):
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

    playing = True

    while playing:
        clearScreenBG(screen,background)
        #This should be where the start menu goes
        #Title.images = load_image("title.gif")
        #print("title image loaded")

        printSCText(150,"Click on a ship to select it for gameplay",screen,green,45)

        quitButton = placeImage("quitB.gif",352,470,screen)
        printSCText(480,"Quit",screen,white,40)

        sY =200
        #this loads the rainbow ship button (in the middle)
        rainbowShip = load_image("shipRainbow.gif")
        xRShip = 352
        yRShip = 200
        screen.blit(rainbowShip,(xRShip,yRShip))
        #pygame.display.flip()

        #This loads the pink ship button to the left
        xPShip = 252
        silverShip = placeImage("shipSilver.gif",xPShip,sY,screen)

        #This loads the green ship button to the right
        xGShip = 452
        greenShip = placeImage("shipGreen.gif",xGShip,sY,screen)

        #Loads the title image
        title = placeImage("titleGame.gif",150,30,screen)
        
        shipType = 0

        notClicked = True
        while (notClicked):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                    x, y = event.pos
                    #mpos = pygame.mouse.get_pos()
                    #print(x,y,xRShip,(xRShip+rainbowShip.get_width()),yRShip,(yRShip+rainbowShip.get_height()))
                    if title.get_rect().collidepoint(x, y):
                        #idk what to do with this one atm but maybe this will launch the github project?
                        webbrowser.open_new("https://github.com/JiahLaBeouf/pyInvaders")

                        #notClicked = False

                    #why does this not work???
                    # if rainbowShip.get_rect().collidepoint(x,y):
                    #     print("clicked on ship")
                    #     notClicked = False

                    #Why the  does this work and not the collidepoint?
                    if xRShip<=x<=(xRShip+rainbowShip.get_width()) and sY<=y<=(sY+rainbowShip.get_height()):
                        shipType = 1
                        notClicked = False
                    elif xPShip <= x <= (xPShip+silverShip.get_width()) and sY <= y <= (sY+silverShip.get_width()):
                        shipType = 0
                        notClicked = False
                    elif xGShip<=x<=(xGShip+96) and sY<=y<=(sY+96):
                        shipType = 2
                        notClicked = False
                    elif collideP(352,470,quitButton,x,y):
                        pygame.quit()
                        sys.exit(0)
                        raise SystemExit
                        return


        screen.blit(background, (0,0))

        #insert start game stuff here

        pygame.mouse.set_visible(0)
        #The ship files are loaded here so that the background and sounds can be initalized for the start menu
        if shipType == 0:
            imgP = load_image('shipSilver.gif')
        elif shipType == 1:
            imgP = load_image('shipRainbow.gif')
        elif shipType == 2:
            imgP = load_image("shipGreen.gif")
        Player.images = [imgP, pygame.transform.flip(imgP, 1, 0)]

        #Loading later to make sure it loads under the player
        img = load_image('base.gif')
        HomeBase.images = [img,pygame.transform.flip(img,1,0)]

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

        lives = 3
        #initialize our starting sprites
        score = 0
        #global LIVES
        player = Player(screenRect)
        Alien(screenRect) #note, this 'lives' because it goes into a sprite group
        if pygame.font:
            all.add(Score(score))
            all.add(Lives(lives))
        homeBase = HomeBase(screenRect)

        maxShots = 4
        
        aliensDead=0

        causeOfDeath = 0

        while player.alive():

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
                                screenRect.size,
                                winstyle | FULLSCREEN,
                                bestdepth
                            )
                            screen.blit(screen_backup, (0, 0))
                        else:
                            print("Changing to windowed mode")
                            screen_backup = screen.copy()
                            screen = pygame.display.set_mode(
                                screenRect.size,
                                winstyle,
                                bestdepth
                            )
                            screen.blit(screen_backup, (0, 0))
                        # screen.fill((255, 0, 0))
                        pygame.display.flip()
                        fullscreen = not fullscreen


            

            # clear/erase the last drawn sprites
            all.clear(screen, background)

            #update all the sprites
            all.update()
            homeBase.update()

            keystate = pygame.key.get_pressed()

            #handle player input
            direction = keystate[K_RIGHT] - keystate[K_LEFT]
            player.move(direction,dt)
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
                Alien(screenRect)
                alienreload = ALIEN_RELOAD
            # Drop bombs
            if lastalien and not int(random.random() * BOMB_ODDS):
                Bomb(lastalien.sprite)

            # Detect collisions
            for alien in pygame.sprite.spritecollide(player, aliens, 1):
                boom_sound.play()
                Explosion(alien)
                Explosion(player)
                score += 1

                screen.blit(background,(0,0))
                pygame.time.wait(1000)

                player.kill()

            for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
                boom_sound.play()
                aliensDead+=1
                if aliensDead%2==0:
                    Bomb(alien)
                Explosion(alien)
                score += 1

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
                
                print("Changing to windowed mode")

                causeOfDeath = 1
                screen.blit(background,(0,0))
                pygame.time.wait(1000)
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
                score += 2
                #Potential powerup for every bomb scored? or possibly for the actual score count.


            if lives==0:
                screen.blit(background,(0,0))
                pygame.time.wait(1000)
                causeOfDeath = 2
                player.kill()

            if keystate[K_k]:
                screen.blit(background,(0,0))
                pygame.display.flip()
                pygame.time.wait(1000)
                causeOfDeath = 3

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

        #THIS is where the endgame goes
        print("about to set to black")
        screen.fill((0,0,0))
        screen.blit(background, (0,0))
        pygame.display.flip()
        #pygame.display.update()
        print("we've blitted the screen now")

        # button = load_image("ship.gif")
        # bx = 300
        # by = 300
        # screen.blit(button,(bx,by))

        # button2 = load_image("shipSHIP.gif")
        # bx2 = 500
        # by2 = 300
        # screen.blit(button,(bx2,by2))
        # pygame.display.update()

        menuButton = placeImage("mainMenu.gif",325,300,screen)
        printSCText(310,"Main Menu",screen,white,40)

        quitButton = placeImage("quitB.gif",352,400,screen)
        printCText(400,"Quit",screen,white)

        printCText(60,"You scored "+str(score)+" points!",screen, white)

        # text_entry = ''

        # error = False
    
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == QUIT:
        #             pygame.quit()
        #             sys.exit()
        #         if event.type == KEYDOWN:
        #             if event.key == K_BACKSPACE:
        #                 text_entry = text_entry[:-1]
        #             elif event.key == K_RETURN:
        #                 pass
        #             else:
        #                 text_entry += event.unicode

        
        if causeOfDeath == 1:
            msg1 = "Cause of death: Homebase was destroyed!"
        elif causeOfDeath == 2:
            msg1 = "Cause of death: Ran out of lives!"
        elif causeOfDeath == 3:
            msg1 = "Cause of death: k pressed!"
        else:
            msg1 = "unknown cause of death"
        printCText(120,msg1,screen,white)
        
        pygame.mouse.set_visible(1)

        replay = True
        while replay == True:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                    x, y = event.pos

                    if collideP(352,400,quitButton,x,y):
                        # pygame.quit()
                        # sys.exit(0)
                        playing = False
                        replay = False
                        

                    elif collideP(325,300,menuButton,x,y):
                        replay = False



    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    #pygame.time.wait(1000)

    pygame.quit()

