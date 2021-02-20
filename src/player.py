import pygame
import toolbox
import projectile
from crate import Crate
from crate import ExplosiveCrate

class Player(pygame.sprite.Sprite):
    #Player constructor function.This is what happens when you make a new player
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("../assets/Player_05.png")
        self.hurtImage = pygame.image.load("../assets/Player_05hurt.png")
        self.defeatedImage = pygame.image.load("../assets/Enemy_05.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 8
        self.angle = 0
        self.shootCooldown = 0
        self.shootCooldownMax = 7
        self.maxHealth = 30
        self.health = self.maxHealth
        self.healthbarWidth = self.image.get_width()
        self.healthbarHeight = 8
        self.healthbarGreen = pygame.Rect(0, 0, self.healthbarWidth, self.healthbarHeight)
        self.healthbarRed = pygame.Rect(0, 0, self.healthbarWidth, self.healthbarHeight)
        self.alive = True
        self.hurtTimer = 0
        self.crateAmmo = 10
        self.explosiveCrateAmmo = 10
        self.crateCooldown = 0
        self.crateCooldownMax = 10
        self.shotType = "normal"
        self.specialAmmo = 0
        self.score = 0

    # Player update function (happens over and over again)
    def update(self, enemies, explosions):
        self.rect.center = (self.x, self.y)

        # Check for collision with players
        for explosion in explosions:
            if explosion.damage and explosion.damagePlayer:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)

        # Check for collision with Enemies
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.getHit(0)
                self.getHit(enemy.damage)

        if self.shootCooldown > 0:
            self.shootCooldown -= 1

        if self.crateCooldown > 0:
            self.crateCooldown -= 1

        # Stop the player from leaving the game screen
        if self.rect.left < 0:
            self.rect.left= 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom > self.screen.get_height()
        self.x = self.rect.centerx
        self.y = self.rect.centery

        if self.alive:
            # Get the angle between the player and the mouse
            mouseX, mouseY = pygame.mouse.get_pos()
            self.angle = toolbox.angleBetweenPoints(self.x, self.y, mouseX, mouseY)

        # Figure out which picture to draw
        if self.alive:
            if self.hurtTimer > 0:
                imageToRotate = self.hurtImage
                self.hurtTimer -= 1
            else:
                imageToRotate = self.image
        else:
            imageToRotate = self.defeatedImage
        
        # Get the rotated version of the player picture
        imageToDraw, imageRect = toolbox.getRotatedImage(imageToRotate, self.rect, self.angle)


        self.screen.blit(imageToDraw, imageRect)
        
        # Move and draw health bar
        self.healthbarRed.x = self.rect.x
        self.healthbarRed.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0), self.healthbarRed)
        self.healthbarGreen.topleft = self.healthbarRed.topleft
        healthPercentage = self.health/self.maxHealth
        self.healthbarGreen.width = self.healthbarWidth * healthPercentage
        if self.alive:
            pygame.draw.rect(self.screen, (0, 255, 0), self.healthbarGreen)
        
    def move(self, xMovement, yMovement, crates):
        if self.alive:
            # Move test rectangle first to see if it collides with a crate.
            testRect = self.rect
            testRect.x += self.speed * xMovement
            testRect.y += self.speed * yMovement
            collision = False
            for crate in crates:
                if not crate.justPlaced:
                    if testRect.colliderect(crate.rect):
                        collision = True

            if not collision:
                self.x += self.speed * xMovement
                self.y += self.speed * yMovement

    # Shoot function
    def shoot(self):
        if self.shootCooldown <= 0 and self.alive:
            if self.shotType == "normal":
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
            elif self.shotType == "splitshot":
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle - 7)
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle)
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle + 7)
                self.shootCooldownMax = 7
                self.specialAmmo -= 1
            elif self.shotType == "stream":
                projectile.WaterDroplet(self.screen, self.x, self.y, self.angle)
                self.specialAmmo -= 1
            elif self.shotType == "bombpotty":
                projectile.ExplosiveWaterBalloon(self.screen, self.x, self.y, self.angle)
                self.specialAmmo -= 1
                
            self.shootCooldown = self.shootCooldownMax
            
            if self.specialAmmo <= 0:
                self.powerUp("normal")

    # GetHit function (makes the player take damage)
    def getHit(self, damage):
        if self.alive:
            self.hurtTimer = 5
            self.health -= damage
            if self.health <= 0:
                # Player ran out of health.
                self.health = 0
                self.alive = False

    def placeCrate(self):
        if self.alive and self.crateAmmo > 0 and self.crateCooldown <= 0:
            Crate(self.screen, self.x, self.y, self)
            self.crateAmmo -= 1
            self.crateCooldown = self.crateCooldownMax

    def placeExplosiveCrate(self):
        if self.alive and self.explosiveCrateAmmo > 0 and self.crateCooldown <= 0:
            ExplosiveCrate(self.screen, self.x, self.y, self)
            self.explosiveCrateAmmo -= 1
            self.crateCooldown = self.crateCooldownMax

    def powerUp(self, powerType):
        if powerType == "crateammo":
            self.crateAmmo += 10
            self.getScore(10)
        elif powerType == "explosiveammo":
            self.explosiveCrateAmmo += 10
            self.getScore(10)
        elif powerType == "health":
            self.health += 10
            self.getScore(10)
            if self.health > self.maxHealth:
                self.health = self.maxHealth
        elif powerType == "splitshot":
            self.shotType = "splitshot"
            self.specialAmmo = 40
            self.shootCooldownMax = 20
            self.getScore(20)
        elif powerType == "normal":
            self.shotType = "normal"
            self.shootCooldownMax = 10
        elif powerType == "stream":
            self.shotType ="stream"
            self.specialAmmo = 300
            self.shootCooldownMax = 3
            self.getScore(20)
        elif powerType == "bombpotty":
            self.shotType = "bombpotty"
            self.specialAmmo = 35
            self.shootCooldownMax = 30
            self.getScore(20)

    def getScore(self, score):
        if self.alive:
            self.score += score







        
