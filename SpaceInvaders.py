import sys
import pygame
from pygame.locals import *
import Invader
import Missile

class SpaceInvaders:

    # Constructor of the basic game class.
    # This constructor calls initialize and main_loop method.
    def __init__(self):
        self.initialize()
        self.main_loop()

    # Initialization method. Allows the game to initialize different
    # parameters and load assets before the game runs
    def initialize(self):
        pygame.init()
        pygame.key.set_repeat(1, 1)

        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.caption = "Space Invader!!"
        pygame.display.set_caption(self.caption)
        
        
        self.framerate = 60

        self.clock = pygame.time.Clock()

        #Set the game state
        self.gameState = 1
        #Initalize the game state method
        self.initializeGameVariables()
        
    def initializeGameVariables(self):
        self.starfieldImg = pygame.image.load('Starfield1024x768.png')
        self.invaderImg = pygame.image.load('inv1.png')
        self.altInvaderImg = pygame.image.load('inv12.png')
        self.rocketLauncherImg = pygame.image.load('LaserBase.png')        
        self.missileImg = pygame.image.load('bullet.png')

        self.rocketXPos = 512
        #self.alienXPos = 512
        #self.alienYPos = 100

        self.alienDirection = +1            
        self.alienSpeed = 10

        #self.missilePosX = - 1
        #self.missilePosY = - 1
        self.missileFired = None

        self.ticks = 0
        #Initalize a list for the invaders.
        self.invaders = []

        #Invaders and rows
        self.noInvader = 9
        self.noRow = 5
        #Set the initial X pos and Y pos for the invaders.
        xPos = 100
        yPos = 100
        #Automatically generate the invaders using a loop.
        for z in range(self.noRow):
            for i in range(self.noInvader):
                invader = Invader.Invader() #Assign variables invader to the class Invader.
                invader.setPosX(xPos) #Set the X position of the first invader.
                invader.setPosY(yPos) #Set Y position of invaders.
                self.invaders.append(invader) #Add invader to the list.
                xPos += 64 #Add 64 onto the invaders X position.
            yPos += 32
            xPos = 100

        #Set font
        self.font = pygame.font.Font(None, 40)

        self.score = 0

    # main loop method keeps the game running. This method continuously
    # calls the update and draw methods to keep the game alive.
    def main_loop(self):
        self.clock = pygame.time.Clock()
        while True:
            gametime = self.clock.get_time()
            self.update(gametime)
            self.draw(gametime)
            self.clock.tick(self.framerate)
            
    def updateStarted(self, gametime):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.gameState = 2
                    break

    def updatePlaying(self,gametime):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] == True or keys[K_d] == True:
            self.rocketXPos = self.rocketXPos + 5
        elif keys[K_LEFT] == True or keys[K_a] == True:
            self.rocketXPos = self.rocketXPos - 5
        elif keys[K_SPACE] == True or keys[K_w] == True and self.missileFired == None:
            #self.missilePosX = self.rocketXPos
            #self.missilePosY = 650 - self.missileImg.get_height()
            #self.missileFired = True
            self.missileFired=Missile.Missile(self.rocketXPos, 650)
        elif keys[K_q] == True:
            pygame.quit()
            sys.exit()

        #Checks whether the missile has been fired.
        #Checks for position of missile in order to fire a second.
        if self.missileFired != None:
            self.missileFired.missileMove()
            if self.missileFired.getPosY() < 0:
                self.missileFired = None
                
        if self.rocketXPos < 100:
            self.rocketXPos = 100

        if self.rocketXPos > 924:
            self.rocketXPos = 924

        self.ticks = self.ticks + gametime

        if self.ticks > 500:
            #Calculate X position of invaders and set speed and direction.
            for i in range(self.noInvader * self.noRow):
                if self.invaders[i] != None:
                    self.invaders[i].moveHorizontal(self.alienSpeed * self.alienDirection)

            leftMostInvader = None
            rightMostInvader = None

            for i in range(self.noInvader):
                if self.invaders[i] != None:
                    rightMostInvader = self.invaders[i]
                    break

            for i in range(self.noInvader -1 , -1, -1):
                if self.invaders[i] != None:
                    rightMostInvader = self.invaders[i]
                    break

            #If the alien in below 96px from the left..    
            if self.invaders[0].getPosX() < 96:
                #Set alien direction vector to positive.
                self.alienDirection = +1
                #Set variable 'xPos' .
                xPos =96
                #Assign I to entities in the range of 11.
                for i in range(self.noInvader * self.noRow):
                    if self.invaders[i] != None:
                        self.invaders[i].moveVertical(10) #Move all invaders in Invaders down by 4.
                        #self.invaders[i].setPosX(xPos) #Set xPos of invaders to 96.
                    xPos = xPos + self.invaderImg.get_width() #Move each invader along by adding it's width.

            #If invader is more than 924px from the left...
            if self.invaders[self.noInvader - 1].getPosX() > 924:
                self.alienDirection = -1 #Set alien direction vector to negative.
                #Set the xPos to 934 - the width of the invader times by ther amount of invaders.
                xPos = 934 - self.invaderImg.get_width() * 8
                #Assign i to a number in the range of 11.
                for i in range(self.noInvader * self.noRow):
                    if self.invaders[i] != None:
                        self.invaders[i].moveVertical(10) #Move all invaders down on the y-axis by 4.
                        #self.invaders[i].setPosX(xPos) #Set the xPos of the invaders based on previous calculation.
                    xPos = xPos + self.invaderImg.get_width() #Move invaders along by adding width.


            for i in range(3, self.noRow):
                for z in range(0,2):
                    if self.invaders[z].getPosY == 210:
                        self.alienSpeed += 2
            """self.invaderSpeed = Invader.Invader()
            if self.invaderSpeed.getPosY() == 200:
                self.alienSpeed += 2
                print(self.alienSpeed)"""

            self.ticks = 0

            #Creating contact areas
            if self.missileFired != None:
                rectMissile = pygame.Rect(self.missileFired.getPosX(), self.missileFired.getPosY(), self.missileImg.get_width(), self.missileImg.get_height())
                for i in range(self.noInvader * 5):
                    if self.invaders[i] != None:
                        rectInvader = pygame.Rect(self.invaders[i].getPosX(), self.invaders[i].getPosY(), self.invaderImg.get_width(), self.invaderImg.get_height())
                        if rectMissile.colliderect(rectInvader):
                            self.missileFired = None
                            self.invaders[i] = None
                            self.score += 10
                            break

    def updateEnded(self, gametime):
        variable = 1

    # Update method contains game update logic, such as updating the game
    # variables, checking for collisions, gathering input, and
    # playing audio.
    def update(self, gametime):
        """#If game state == 1, start loading screen.
        if self.gameState == 1:
            self.updateStarted(self)
        #If game state = 2, start actual game play
        elif self.gameState == 2:
            self.updatePlaying(self)
        #If game state = 3, end the game.
        elif self.gameState == 3:
            self.updateEnded(self)"""

        if self.gameState == 1:
            self.updateStarted(gametime)
        elif self.gameState == 2:
            self.updatePlaying(gametime)
        elif self.gameState == 3:
            self.updateEnded(gametime)

        

    def drawStarted(self, gametime):
        
        self.screen.blit(self.starfieldImg, (0,0))
        #Font drawing
        width, height = self.font.size("S P A C E  I V A D E R S")
        text = self.font.render("S P A C E  I V A D E R S", True, (255, 0, 0))
        xPos = (1024 - width) / 2
        self.screen.blit(text, (xPos, 300))

        width, height = self.font.size("P R E S S  'S'  T O  S T A R T")
        text = self.font.render("P R E S S  'S'  T O  S T A R T", True, (255, 0, 0))
        xPos = (1024 - width) / 2
        self.screen.blit(text, (xPos, 400))

        pygame.display.flip()

    def drawPlaying(self, gametime):
        self.screen.blit(self.starfieldImg, (0,0))

        #Font drawing
        width, height = self.font.size("SCORE:")
        text = self.font.render("SCORE: %d" %self.score, True, (255, 0, 0))
        xPos = 10
        self.screen.blit(text, (xPos, 10))
        
        self.screen.blit(self.rocketLauncherImg, (self.rocketXPos, 650))

        if self.missileFired != None:
            self.screen.blit(self.missileImg, (self.missileFired.getPosX(), self.missileFired.getPosY() - self.missileImg.get_height()))
        
        for i in range(self.noInvader * self.noRow):
            if self.invaders[i] != None:
                self.screen.blit(self.invaderImg, self.invaders[i].getPosition())
        pygame.display.flip()

    def drawEnded(self, gametime):
        variable = 1
        

    # Draw method, draws the current state of the game on the screen                        
    def draw(self, gametime):

        #If game state = 1, draw start screen.
        if self.gameState == 1:
            self.drawStarted(gametime)
        #If game state = 2, draw active game.
        elif self.gameState == 2:
            self.drawPlaying(gametime)
        #If game state = 3, draw end screen.
        elif self.gameState == 3:
            self.drawEnded(gametime)
        

        pygame.display.flip()



if __name__ == "__main__":
    game = SpaceInvaders()
