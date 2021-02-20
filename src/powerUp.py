import pygame
import random
import toolbox

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.pickPower = random.randint(0, 5)
        if self.pickPower == 0: # Crate Ammo
            self.image = pygame.image.load("../assets/powerupCrate.png")
            self.backgroundImage = pygame.image.load("../assets/powerupBackgroundBlue.png")
            self.powerType = "crateammo"
        elif self.pickPower == 1: # Explosive Crate Ammo
            self.image = pygame.image.load("../assets/powerupExplosiveBarrel.png")
            self.backgroundImage = pygame.image.load("../assets/powerupBackgroundBlue.png")
            self.powerType = "explosiveammo"
        elif self.pickPower == 2: # Health # Andy didn't do this one
            self.image = pygame.image.load("../assets/RedCrossAdobe.png")
            self.backgroundImage = pygame.image.load("../assets/powerupBackgroundBlue.png")
            self.powerType = "health"
        elif self.pickPower == 3: # Split Shot
            self.image = pygame.image.load("../assets/powerupSplitGreen.png")
            self.backgroundImage = pygame.image.load("../assets/powerupBackgroundRed.png")
            self.powerType = "splitshot"
        elif self.pickPower == 4: # Stream
            self.image = pygame.image.load("../assets/powerupDrop.png")
            self.backgroundImage = pygame.image.load("../assets/powerupBackgroundRed.png")
            self.powerType = "stream"
        elif self.pickPower == 5: # Bomb Potty
            self.image = pygame.image.load("../assets/SplashSmall1.png")
            self.backgroundImage = pygame.image.load("../assets/powerupBackgroundRed.png")
            self.powerType = "bombpotty"
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.backgroundAngle = 0
        self.spinSpeed = 2
        self.despawnTimer = 600

    def update(self, player):
        if self.rect.colliderect(player.rect):
            player.powerUp(self.powerType)
            self.kill()

        self.despawnTimer -= 1
        if self.despawnTimer <= 0:
            self.kill()
        
        self.backgroundAngle += self.spinSpeed
        bgImageToDraw, bgRect = toolbox.getRotatedImage(self.backgroundImage, self.rect, self.backgroundAngle)

        if self.despawnTimer > 135 or self.despawnTimer % 10 > 5:
            self.screen.blit(bgImageToDraw, bgRect)
            self.screen.blit(self.image, self.rect)
