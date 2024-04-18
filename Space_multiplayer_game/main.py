import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))


# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('shuttle.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = random.randint(0,736)
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('game.png')
enemyX = random.randint(0, 736)
enemyY = 50
enemyX_change = 0  # Change to control enemy movement in X-axis

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# EnemyBullet
enemy_bulletIMG =pygame.image.load('bulletrev.png')
enemy_bulletX = 0
enemy_bulletY = enemyY
enemy_bulletY_change = 10
enemy_bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 550

# Bottom Score
enemy_score = 0
bottom_textX = 10
bottom_textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_bottom_score(x, y):
    score = font.render("Enemy Score : " + str(enemy_score), True, (0, 0, 0))
    screen.blit(score, (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def fire_enemy_bullet(x, y):
    global enemy_bullet_state
    enemy_bullet_state = "fire"
    screen.blit(enemy_bulletIMG , (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY):
    enemy_distance = math.sqrt(math.pow(playerX - enemy_bulletX, 2) + (math.pow(playerY - enemy_bulletY, 2)))
    if enemy_distance < 27:
        return True
    else:
        return False


game_break=False
# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((255,255, 255))
    # Background Image
    #screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


        # Enemy movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                enemyX_change = -1
            if event.key == pygame.K_d:
                enemyX_change = 1
            if event.key == pygame.K_w:
                if enemy_bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    enemy_bulletX = enemyX
                    fire_enemy_bullet(enemy_bulletX, enemy_bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                enemyX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX = 0
    elif enemyX >= 736:
        enemyX = 736

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy Bullet movement
    if enemy_bulletY >= 600:
        enemy_bulletX= enemyX
        enemy_bulletY = enemyY
        enemy_bullet_state = "ready"

    if enemy_bullet_state == "fire":
        fire_enemy_bullet(enemy_bulletX, enemy_bulletY)
        enemy_bulletY += enemy_bulletY_change


    #game break
    
    

    #winner show
    if ((score_value==2)or (enemy_score==2)):
        if((score_value==2)):
            over_text = over_font.render("PLAYER WIN", True, (0, 0, 0))
            screen.blit(over_text, (200, 250))
            game_break=True
           
        else:
            over_text = over_font.render("ENEMY WIN", True, (0, 0, 0)) 
            screen.blit(over_text, (200, 250))
            game_break=True
            

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    player_hit = isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY)

    if collision and not game_break:
        explosionSound = mixer.Sound("explosion.wav")
        explosionSound.play()
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = 50

    if player_hit and not game_break:
    # Player got hit by enemy bullet
    # You can handle player hit logic here, such as reducing player health or ending the game
        explosionSound = mixer.Sound("explosion.wav")
        explosionSound.play()
        enemy_bulletY = 50
        enemy_bullet_state = "ready"
        enemy_score += 1
        playerX = random.randint(0, 736)
        playerY = 480

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, textY)
    show_bottom_score(bottom_textX,bottom_textY)
    pygame.display.update()
