import pygame
import toolbox

class HUD():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.state = "mainmenu"

        self.hudFont = pygame.font.SysFont("onyx", 30)
        self.hudFontM = pygame.font.SysFont("default", 30)
        self.hudFontBig = pygame.font.SysFont("default", 80)

        self.scoreText = self.hudFont.render("Potty", True, (255, 255, 255))

        # Load stuff for the main menu
        self.titleImage = pygame.image.load("../assets/Title.png")
        self.startBlinkTimerMax = 40
        self.startBlinkTimer = self.startBlinkTimerMax
        self.startText = self.hudFont.render("Press any key to start", True, (255, 255, 255))
        self.tutorialText = self.hudFontM.render("WASD to move - LEFT CLICK to shoot - SPACE for crate - RIGHT CLICK for explosive crate", True, (255, 255, 255))

        # Load the stuff for the gamover screen
        self.gameOverText = self.hudFontBig.render("Game Over", True, (6, 54, 82))
        self.resetButton = pygame.image.load("../assets/BtnReset.png")

        # Load the images for ammo tiles
        self.crateIcon = pygame.image.load("../assets/Crate.png")
        self.explosiveBarrelIcon = pygame.image.load("../assets/ExplosiveBarrel.png")
        self.splitShotIcon = pygame.image.load("../assets/iconSplitGreen.png")
        self.streamShotIcon = pygame.image.load("../assets/iconStream.png")
        self.bombShotIcon = pygame.image.load("../assets/iconBurstGreen.png")
        self.normalShotIcon = pygame.image.load("../assets/BalloonSmallEdited.png")
        
        # Make all the ammo tiles
        self.crateAmmoTile = AmmoTile(self.screen, self.crateIcon, self.hudFont)
        self.explosiveCrateAmmoTile = AmmoTile(self.screen, self.explosiveBarrelIcon, self.hudFont)
        self.balloonAmmoTile = AmmoTile(self.screen, self.normalShotIcon, self.hudFont)

    def update(self):
        if self.state == "ingame":
            # Draw the score text
            self.scoreText = self.hudFont.render("Score: " + str(self.player.score), True, (255, 255, 255))
            self.screen.blit(self.scoreText, (10, 10))

            # Draw the ammo tiles
            tileX = 0
            self.crateAmmoTile.update(tileX, self.screen.get_height(), self.player.crateAmmo)
            tileX += self.crateAmmoTile.width
            self.explosiveCrateAmmoTile.update(tileX, self.screen.get_height(), self.player.explosiveCrateAmmo)
            tileX += self.explosiveCrateAmmoTile.width
            
            # Figure out which icon to use
            if self.player.shotType == "normal":
                self.balloonAmmoTile.icon = self.normalShotIcon
            elif self.player.shotType == "splitshot":
                self.balloonAmmoTile.icon = self.splitShotIcon
            elif self.player.shotType == "stream":
                self.balloonAmmoTile.icon = self.streamShotIcon
            elif self.player.shotType == "bombpotty":
                self.balloonAmmoTile.icon = self.bombShotIcon
            
            self.balloonAmmoTile.update(tileX, self.screen.get_height(), self.player.specialAmmo)

        elif self.state == "mainmenu":
            self.startBlinkTimer -= 1
            if self.startBlinkTimer <= 0:
                self.startBlinkTimer = self.startBlinkTimerMax
            titleX, titleY = toolbox.centeringCoords(self.titleImage, self.screen)
            self.screen.blit(self.titleImage, (titleX, titleY))
            textX, textY = toolbox.centeringCoords(self.startText, self.screen)
            if self.startBlinkTimer > 20:
                self.screen.blit(self.startText, (textX, textY + 150))
            textX, textY = toolbox.centeringCoords(self.tutorialText, self.screen)
            textY += 250
            self.screen.blit(self.tutorialText, (textX, textY))

        elif self.state == "gameover":
            textX, textY = toolbox.centeringCoords(self.gameOverText, self.screen)
            textY -= 140
            self.screen.blit(self.gameOverText, (textX, textY))
            self.scoreText = self.hudFont.render("Final Score: " + str(self.player.score), True, (255, 255, 255))
            textX, textY = toolbox.centeringCoords(self.scoreText, self.screen)
            textY -= 85
            self.screen.blit(self.scoreText, (textX, textY))
            buttonX, buttonY = toolbox.centeringCoords(self.resetButton, self.screen)
            buttonY += 40
            buttonRect = self.screen.blit(self.resetButton, (buttonX, buttonY))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePosition = pygame.mouse.get_pos()
                    if buttonRect.collidepoint(mousePosition):
                        self.state = "mainmenu"

class AmmoTile():
    def __init__(self, screen, icon, font):
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bgImage = pygame.image.load("../assets/hudTile.png")
        self.width = self.bgImage.get_width()

    def update(self, x, y, ammo):
        # Draw tile background
        tileRect = self.bgImage.get_rect()
        tileRect.bottomleft = (x, y)
        self.screen.blit(self.bgImage, tileRect)
        
        # Draw icon
        iconRect = self.icon.get_rect()
        iconRect.center = tileRect.center
        self.screen.blit(self.icon, iconRect)
        
        # Draw ammo amount
        ammoText = self.font.render(str(ammo), True, (255, 255, 255))
        self.screen.blit(ammoText, tileRect.topleft)
        


        
