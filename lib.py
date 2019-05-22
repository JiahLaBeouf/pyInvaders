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

class Timer(pygame.sprite.Sprite):
    #score = None
    def __init__(self,inGameTime):
        pygame.sprite.Sprite.__init__(self)
        #self.score = score
        self.font = pygame.font.Font(None, 50)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lasttime = -1
        self.update()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect().move(((800-self.width)/2), 20)

    def update(self):
        if self.lasttime != inGameTime:
            self.lasttime = inGameTime
            msg = "Time: %d" % inGameTime
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
    
    img = loadImage('explosion1.gif')
    Explosion.images = [img, pygame.transform.flip(img, 1, 1)]
    Alien.images = loadImages('alien1.gif', 'alien2.gif', 'alien3.gif')
    Bomb.images = [loadImage('bomb.gif')]
    Shot.images = [loadImage('shot.png')]
    Health.images = [loadImage('health.gif')]

    #decorate the game window
    icon = pygame.transform.scale(Alien.images[0], (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Jiah Presents: PyInvaders! (V1.1)')

    #create the background, tile the bgd image
    bgdtile = loadImage('hubbleimage.png')
    background = pygame.Surface(screenRect.size)
    for x in range(0, screenRect.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #load the sound effects
    boom_sound = loadSound('boom.wav')
    shoot_sound = loadSound('laserSound.wav')
    #healthSound = loadSound('powerUp1.wav')
    if pygame.mixer:
        music = os.path.join(mainDir, 'data', 'gameMusic2.wav')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    playing = True

    tFile = open("leaderboard.txt",'r+')

    

    while playing:
        clearScreenBG(screen,background)

        printSCText(150,"Click on a ship to select it for gameplay",screen,green,45)

        quitButton = placeImage("quitB.gif",352,470,screen)
        printSCText(480,"Quit",screen,white,40)

        sY =200
        #this loads the rainbow ship button (in the middle)
        rainbowShip = loadImage("shipRainbow.gif")
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

        names = []
        scores = []
        tFile = open("leaderboard.txt",'r+')
        list = tFile.read().splitlines()
        iterator = True
        i=int(0)
        ender = len(list)-1
        while iterator:
            name,scorez = list.pop(0).split("|")
            names.append(name)
            scores.append(int(scorez))
            i = i+1
            #print(i)
            if i>ender:
                iterator = False
            else:
                x = 1

        n = len(scores)

        for i in range(n):
         
            # Last i elements are already in place
            for j in range(0, n-i-1):
     
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if scores[j] < scores[j+1] :
                    scores[j], scores[j+1] = scores[j+1], scores[j]
                    names[j],names[j+1]=names[j+1],names[j]

        msgLB1 = names[0]+": "+str(scores[0])
        msgLB2 = names[1]+": "+str(scores[1])
        msgLB3 = names[2]+": "+str(scores[2])

        printCText(310,"HIGH SCORES",screen,green)
        printSCText(360,msgLB1,screen,white,30)
        printSCText(390,msgLB2,screen,white,30)
        printSCText(420,msgLB3,screen,white,30)

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

        clearScreenBG(screen,background)


        #Starting the layout for the game difficulty screen
        
        #Places the two independent captions
        printSCText(80,"Select Game Difficulty",screen,green,75)
        printSCText(400,"Game controls will appear once difficulty selected",screen,white,30)

        easy = placeImage("easy.gif",216,200,screen)
        printText(218,205,"Easy",screen,white)

        medium = placeImage("medium.png",340,200,screen)
        printCText(205,"Medium",screen,white)

        hard = placeImage("hard.gif",488,200,screen)
        printText(490,205,"Hard",screen,white)

        difficulty = None

        #This while loop is where the difficulty is determined
        #This uses the self made collideP method to detect mouse clicks on objects.
        difficultyChoice = True
        while (difficultyChoice):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                    x, y = event.pos
                    
                    if collideP(216,200,easy,x,y):
                        difficulty = 0
                        difficultyChoice = False
                    elif collideP(340,200,medium,x,y):
                        difficulty = 1
                        difficultyChoice = False
                    elif collideP(488,200,hard,x,y):
                        difficulty = 2
                        difficultyChoice = False

        clearScreenBG(screen,background)

        #This loads the control screen and blits to cover screen.
        sc1 = loadImage("controls.gif")
        clearScreenBG(screen,sc1)

        #This is the controls screen, which waits for a click anywhere, hence no collide methods.
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                
                    clicked = True


        clearScreenBG(screen,background)

        #The mouse is now set invisible so that there is no interruption to gameplay
        pygame.mouse.set_visible(0)

        img = loadImage('base.gif')
        HomeBase.images = [img,pygame.transform.flip(img,1,0)]

        #The ship is now loaded based on earlier preference from the start menu.
        if shipType == 0:
            imgP = loadImage('shipSilver.gif')
        elif shipType == 1:
            imgP = loadImage('shipRainbow.gif')
        elif shipType == 2:
            imgP = loadImage("shipGreen.gif")
        Player.images = [imgP, pygame.transform.flip(imgP, 1, 0)]

        


        # Initialize Game Groups
        aliens = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        bombs = pygame.sprite.Group()
        healths = pygame.sprite.Group()
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
        Timer.containers = all
        Health.containers = healths, all

        #Create Some Starting Values, as well as initialising global variables for the sprites during gameplay
        global score
        global inGameTime
        global lives
        framesPerAlien = ALIEN_RELOAD
        kills = 0
        clock = pygame.time.Clock()
        lives = 3
        inGameTime = 0
        score = 0

        #Init starting sprites (or 'living sprites')
        player = Player(screenRect)
        Alien(screenRect) #this 'lives' because it goes into a sprite group

        #adding the value sprites to the game screen
        if pygame.font:
            all.add(Score(score))
            all.add(Lives(lives))
            all.add(Timer(inGameTime))

        #adding the homebase, passes in the screen so it can determine it's staring position.
        homeBase = HomeBase(screenRect)

        #This has the potential to be proportional to the score if more challenge is required
        maxShots = 4
        
        aliensDead=0

        #Used later, in the endgame menu
        causeOfDeath = 0

        startTime = pygame.time.get_ticks()

        #This loop is essentially the gameplay loop. It ends whenever the player is killed
        while player.alive():

            inGameTime = round(((pygame.time.get_ticks()) - startTime)/1000)


            #Increasing difficulty rate here. Uses the time to determine how many aliens spawn and when
            
            #Easy difficulty. Never changes, this has room for improvement
            if difficulty == 0:
                if inGameTime<=10:
                    alienReload = 7
                
            #Medium difficulty
            elif difficulty == 1:
                if inGameTime<=10:
                    alienReload = 6
                elif 10<=inGameTime<=120:
                    #This specific range is due to the divisor, to avoid rounding to zero.
                    alienReload = round(6/((inGameTime/10)+0.001))
                else:
                    alienReload = 2

            #Hard difficulty
            elif difficulty == 2:
                if inGameTime<=10:
                    alienReload = 6
                elif 10<=inGameTime<=70:
                    #This specific range is due to the divisor, to avoid rounding to zero.
                    alienReload = round(6/(inGameTime/6)+0.01)
                else:
                    alienReload = 1

            

            #get input to determine quitting application or changing to fullscreen. May depreciate this.
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

            #handle player input to determine character movement.
            direction = keystate[K_RIGHT] - keystate[K_LEFT]
            player.move(direction,dt)

            #This is incase of 2 player and/or random movement, currently homebase has 0 velocity but this could change in the future
            direction2 = keystate[K_UP] - keystate[K_DOWN]
            homeBase.move(direction2)

            #The firing code
            firing = keystate[K_SPACE]
            if not player.reloading and firing and len(shots) < maxShots:
                Shot(player.gunpos())
                shoot_sound.play()
            player.reloading = firing

            # Create new alien

            odds = int(random.random() * ALIEN_ODDS)

            if framesPerAlien>=0:
                framesPerAlien = framesPerAlien - 1
            elif odds ==0:
                #This basically gives the odds of an alien showing up.
                Alien(screenRect)
                framesPerAlien = alienReload
            # Drop bombs
            if lastalien and not int(random.random() * BOMB_ODDS):
                Bomb(lastalien.sprite)

            # Detect collisions

            #This is for if an alien reaches a player, which results in instant death.
            for alien in pygame.sprite.spritecollide(player, aliens, 1):
                boom_sound.play()
                Explosion(alien)
                Explosion(player)
                score += 1

                screen.blit(background,(0,0))
                pygame.time.wait(1000)

                player.kill()

            #Bullet and alien collision
            for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
                boom_sound.play()
                aliensDead+=1
                if aliensDead%2==0:
                    Bomb(alien)
                Explosion(alien)
                if aliensDead%10 == 0:
                    Health(alien)
                score += 1

            #bomb hitting player
            for bomb in pygame.sprite.spritecollide(player, bombs, 1):
                boom_sound.play()
                Explosion(player)
                Explosion(bomb)
                #player.kill()
                lives-=1

            #Player collecting health
            for health in pygame.sprite.spritecollide(player,healths,1):
                #healthSound.play()
                lives +=1
                health.kill()
                #play health up sound if interviews suggest it

            #Bombing home base
            for bomb in pygame.sprite.spritecollide(homeBase, bombs, 1):
                boom_sound.play()
                Explosion(homeBase)
                Explosion(bomb)
                causeOfDeath = 1
                player.kill()

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

        menuButton = placeImage("mainMenu.gif",325,300,screen)
        printSCText(310,"Main Menu",screen,white,40)

        quitButton = placeImage("quitB.gif",352,400,screen)
        printCText(400,"Quit",screen,white)

        printCText(60,"You scored "+str(score)+" points!",screen, white)
        
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

        textEntry = ''

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

        printCText(200,"Enter Name:            ",screen,green)

        replay = True
        while replay == True:

            printText(400,200,textEntry,screen,white)

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
                elif event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        textEntry = text_entry[:-1]
                    elif event.key == K_RETURN:
                        pass
                    else:
                        textEntry += event.unicode

        nameW = str(textEntry)

        tFile.write("\n"+nameW+"|"+str(score))



    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)

    pygame.quit()

