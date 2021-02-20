import pygame
import random
from powerUp import PowerUp
import toolbox
import math
from explosion import Explosion

class Enemy(pygame.sprite.Sprite):
    # Enemy constructor function
    def __init__(self, screen, x, y, player):
        # Make enemy inherit sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        # Setting up the enemy variables
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("../assets/Enemy_02.png")
        self.imageHurt = pygame.image.load("../assets/Enemy_02hurt.png")
        self.explosionImages = []
        self.explosionImages.append(pygame.image.load("../assets/MediumExplosion1.png"))
        self.explosionImages.append(pygame.image.load("../assets/MediumExplosion2.png"))
        self.explosionImages.append(pygame.image.load("../assets/MediumExplosion3.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.speed = 1
        self.health = 23
        self.hurtTimer = 0
        self.damage = 1
        self.obstacleAnger = 0
        self.obstacleAngerMax = 100
        self.powerUpDropChance = 50 # Out of 100

    def update(self, projectiles, crates, explosions):
        # Figure out the angle between the enemy and the player
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)

        # Move the enemy in the direction it is facing
        angleRads = math.radians(self.angle)
        self.xMove = math.cos(angleRads) * self.speed
        self.yMove = -math.sin(angleRads) * self.speed

        # Check to see if the enemy is gonna run into a crate
        testRect = self.rect
        newX = self.x + self.xMove
        newY = self.y + self.yMove

        testRect.center = (newX, self.y)
        for crate in crates:
            if testRect.colliderect(crate.rect):
                newX = self.x
                self.getAngry(crate)

        testRect.center = (self.x, newY)
        for crate in crates:
            if testRect.colliderect(crate.rect):
                newY = self.y
                self.getAngry(crate)
        
        self.x = newX
        self.y = newY
        self.rect.center = (self.x, self.y)

        # Check for collisions with explosions
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)

        # Checks for collisions with projectiles
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)
                projectile.explode()

        if self.hurtTimer <= 0:
            imageToRotate = self.image
        else:
            imageToRotate = self.imageHurt
            self.hurtTimer -= 1

        imageToDraw, imageRect = toolbox.getRotatedImage(imageToRotate, self.rect, self.angle)

        self.screen.blit(imageToDraw, imageRect)

    def getHit(self, damage):
        if damage:
            self.hurtTimer = 5
        self.x -= self.xMove * 7
        self.y -= self.yMove * 7
        self.health -= damage
        if self.health <= 0:
            # Set health very high so self.kill only happens once
            self.health = 99999
            self.player.getScore(50)
            Explosion(self.screen, self.x, self.y, self.explosionImages, 5, 0, False)

            if random.randint(0, 100) < self.powerUpDropChance:
                PowerUp(self.screen, self.x, self.y)
            
            self.kill()

    def getAngry(self, crate):
        self.obstacleAnger += 1
        if self.obstacleAnger >= self.obstacleAngerMax:
            crate.getHit(self.damage)
            self.obstacleAnger = 0


