import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, images, duration, damage, damagePlayer):
        # Make explosion inherit Sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        # Set up explosion variables
        self.screen = screen
        self.y = y
        self.x = x
        self.images = images
        self.duration = duration
        self.damage = damage
        self.damagePlayer = damagePlayer
        self.rect = self.images[0].get_rect()
        self.rect.center = (self.x, self.y)
        self.animationTimer = duration
        self.frameToDraw = 0
        self.lastFrame = len(self.images) - 1
        
    def update(self):
        self.animationTimer -= 1
        if self.animationTimer <= 0:
            if self.frameToDraw < self.lastFrame:
                self.frameToDraw += 1
                self.animationTimer = self.duration
            else:
                self.kill()
        
        self.screen.blit(self.images[self.frameToDraw], self.rect)
