import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from explosion import Explosion
from powerUp import PowerUp
from hud import HUD

# Start the game
pygame.init()
gameWidth = 1000
gameHeight = 650
screen = pygame.display.set_mode((gameWidth, gameHeight))
clock = pygame.time.Clock()
running = True

backgroundImg = pygame.image.load("../assets/BG_Mars.png")

# Make all the Sprite groups
playerGroup = pygame.sprite.Group()
projectilesGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
cratesGroup = pygame.sprite.Group()
explosionsGroup = pygame.sprite.Group()
powerupsGroup = pygame.sprite.Group()

# Put every Sprite class in a group
Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Crate.conatainers = cratesGroup
Explosion.containers = explosionsGroup
PowerUp.containers = powerupsGroup

enemySpawnTimerMax = 100
enemySpawnTimer = 0
enemySpawnSpeedupTimerMax = 400
enemySpawnSpeedupTimer = enemySpawnSpeedupTimerMax

gameStarted = False

mrPlayer = Player(screen, gameWidth/2, gameHeight/2)

hud = HUD(screen, mrPlayer)

# StartGame function makes the game switch from mainmenu in ingame
def startGame():
    global gameStarted
    global hud
    global mrPlayer
    global enemySpawnTimerMax
    global enemySpawnTimer
    global enemySpawnSpeedupTimer

    enemySpawnTimerMax = 100
    enemySpawnTimer = 0
    enemySpawnSpeedupTimer = enemySpawnSpeedupTimerMax
    
    gameStarted = True
    hud.state = "ingame"
    mrPlayer.__init__(screen, gameWidth/2, gameHeight/2)

    for i in range(0, 20):
        num = random.randint(1, 2)
        if num == 1:
            ExplosiveCrate(screen, random.randint(0, gameWidth), random.randint(0, gameHeight), mrPlayer)
        else:
            Crate(screen, random.randint(0, gameWidth), random.randint(0, gameHeight), mrPlayer)

# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    screen.blit(backgroundImg, (0, 0))

    if not gameStarted:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                startGame()
                break

    if gameStarted:
        # Deal with the player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            mrPlayer.move(1, 0, cratesGroup)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            mrPlayer.move(-1, 0, cratesGroup)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            mrPlayer.move(0, -1, cratesGroup)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            mrPlayer.move(0, 1, cratesGroup)
        if pygame.mouse.get_pressed()[0]:
            mrPlayer.shoot()
        if keys[pygame.K_SPACE]:
            mrPlayer.placeCrate()
        if pygame.mouse.get_pressed()[2]:
            mrPlayer.placeExplosiveCrate()

        enemySpawnSpeedupTimer -= 1
        if enemySpawnSpeedupTimer <= 0:
            if enemySpawnTimerMax > 20:
                enemySpawnTimerMax -= 10
                enemySpawnSpeedupTimer = enemySpawnSpeedupTimerMax

        # Make Enemy Spawning happen
        enemySpawnTimer -= 1
        if enemySpawnTimer <= 0:
            newEnemy = Enemy(screen, 0, 0, mrPlayer)
            sideToSpawn = random.randint(0, 3) #0=top, 1=bottom, 2=left, 3=right
            if sideToSpawn == 0:
                newEnemy.x = random.randint(0, gameWidth)
                newEnemy.y = -newEnemy.image.get_height()
            elif sideToSpawn == 1:
                newEnemy.x = random.randint(0, gameWidth)
                newEnemy.y = gameHeight + newEnemy.image.get_height()
            elif sideToSpawn == 2:
                newEnemy.x = -newEnemy.image.get_width()
                newEnemy.y = random.randint(0, gameHeight)
            elif sideToSpawn == 3:
                newEnemy.x = gameWidth + newEnemy.image.get_width()
                newEnemy.y = random.randint(0, gameHeight)
            enemySpawnTimer = enemySpawnTimerMax
                
        for powerup in powerupsGroup:
            powerup.update(mrPlayer)

        for projectile in projectilesGroup:
            projectile.update()

        for enemy in enemiesGroup:
            enemy.update(projectilesGroup, cratesGroup, explosionsGroup)

        for crate in cratesGroup:
            crate.update(projectilesGroup, explosionsGroup)

        for explosion in explosionsGroup:
            explosion.update()

        mrPlayer.update(enemiesGroup, explosionsGroup)

        if not mrPlayer.alive:
            if hud.state == "ingame":
                hud.state = "gameover"
            elif hud.state == "mainmenu":
                gameStarted = False
                playerGroup.empty()
                enemiesGroup.empty()
                projectilesGroup.empty()
                explosionsGroup.empty()
                cratesGroup.empty()
                powerupsGroup.empty()

    hud.update()

    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("Robo Invasion fps: " + str(clock.get_fps()))
