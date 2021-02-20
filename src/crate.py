import pygame
from explosion import Explosion

class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.conatainers)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("../assets/Crate.png")
        self.imageHurt = pygame.image.load("../assets/CrateHurt.png")
        self.explosionImages = []
        self.explosionImages.append(pygame.image.load("../assets/CrateRubble.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 50
        self.hurtTimer = 0
        self.justPlaced = True

    def update(self, projectiles, explosions):
        if not self.rect.colliderect(self.player.rect):
            self.justPlaced = False

        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)
        
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                projectile.explode()
                self.getHit(projectile.damage)
                
        if self.hurtTimer > 0:
            self.hurtTimer -= 1
            imageToDraw = self.imageHurt
        else:
            imageToDraw = self.image

        
        self.screen.blit(imageToDraw, self.rect)

    def getHit(self, damage):
        self.health -= damage
        self.hurtTimer = 5
        if self.health <= 0:
            self.health = 99999
            Explosion(self.screen, self.x, self.y, self.explosionImages, 20, 0, False)
            self.kill()


class ExplosiveCrate(Crate):
    def __init__(self, screen, x, y, player):
        Crate.__init__(self, screen, x, y, player)
        self.health = 20
        self.image = pygame.image.load("../assets/ExplosiveBarrel.png")
        self.imageHurt = pygame.image.load("../assets/ExplosiveBarrelHurt.png")
        self.explosionImages = []
        self.explosionImages.append(pygame.image.load("../assets/LargeExplosion1.png"))
        self.explosionImages.append(pygame.image.load("../assets/LargeExplosion2.png"))
        self.explosionImages.append(pygame.image.load("../assets/LargeExplosion3.png"))

    def getHit(self, damage):
        self.health -= damage
        self.hurtTimer = 5
        if self.health <= 0:
            self.health = 99999
            Explosion(self.screen, self.x, self.y, self.explosionImages, 5, 4, True)
            self.kill()
        
