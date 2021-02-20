import pygame
import toolbox
import math
from explosion import Explosion

class WaterBalloon(pygame.sprite.Sprite):
    # Water Balloon constructor function
    def __init__(self, screen, x, y, angle):
        # Make water balloon sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        # Set up water balloon variable
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load("../assets/BalloonSmallEdited.png")
        self.explosionImages = []
        self.explosionImages.append(pygame.image.load("../assets/SplashSmall1.png"))
        self.explosionImages.append(pygame.image.load("../assets/SplashSmall2.png"))
        self.explosionImages.append(pygame.image.load("../assets/SplashSmall3.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.speed = 10
        self.angleRads = math.radians(self.angle)
        self.xMove = math.cos(self.angleRads) * self.speed
        self.yMove = -math.sin(self.angleRads) * self.speed
        self.damage = 6

    def update(self):
        self.x += self.xMove
        self.y += self.yMove
        self.rect.center = (self.x, self.y)

        # Remove the balloon if it goes to far off the screen
        if self.x < -self.image.get_width():
            self.kill()
        elif self.x > self.screen.get_width() + self.image.get_width():
            self.kill()
        elif self.y < -self.image.get_height():
            self.kill()
        elif self.y > self.screen.get_height() + self.image.get_width():
            self.kill()
        
        self.screen.blit(self.image, self.rect)
        
    def explode(self):
        Explosion(self.screen, self.x, self.y, self.explosionImages, 5, 0, False)
        self.kill()

class SplitWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("../assets/BalloonSmallGreen.png")
        self.damage = 8
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)

class WaterDroplet(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("../assets/DropSmall.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.damage = 3

class ExplosiveWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("../assets/BalloonTNT.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.explosionImages = []
        self.explosionImages.append(pygame.image.load("../assets/LargeExplosion1.png"))
        self.explosionImages.append(pygame.image.load("../assets/LargeExplosion2.png"))
        self.explosionImages.append(pygame.image.load("../assets/LargeExplosion3.png"))

    def explode(self):
      Explosion(self.screen, self.x, self.y, self.explosionImages, 4, 2, False)
      self.kill()  
