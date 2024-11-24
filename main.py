import pygame
import sys
from player import Player
from mustache import Mustache
from block import Block

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.Channel(0).play(pygame.mixer.Sound('music.mp3'))

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
GROUND_Y = SCREEN_HEIGHT - 50
FPS = 120

background_image = pygame.image.load("Assets/background.jpg")
scaled_background = pygame.transform.scale(background_image, (1200, 800))

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Evil Twin")
clock = pygame.time.Clock()

# Create objects
player1 = Player(100, GROUND_Y - 100)
player2 = Player(1000, GROUND_Y - 100, delay=0, lives=5, direction=-1)  # Delayed input
mustache = Mustache()
ground = Block(0, 750, 1200, 50, "Assets/block.png")
block1 = Block(600, 400, 500, 60, "Assets/block.png")
block2 = Block(50, 300, 150, 60, "Assets/block.png")
block3 = Block(350, 600, 300, 300, "Assets/block.png")
block4 = Block(400, 200, 200, 60, "Assets/block.png")
blocks = [block1, block2, block3, block4, ground]

# Game loop
running = True
while running:

    # Blit the scaled image to the screen at (0, 0)
    screen.blit(scaled_background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input handling for player1
    keys = pygame.key.get_pressed()
    player1_movement = (0, 0)
    if keys[pygame.K_LEFT]:  # Move left
        player1_movement = (-3, 0)
        player1.direction = -1
    if keys[pygame.K_RIGHT]:  # Move right
        player1_movement = (3, 0)
        player1.direction = 1

    if keys[pygame.K_f]:  # Block
        player1.update("block", player1_movement, player2, keys, blocks)
    elif keys[pygame.K_SPACE]:  # Attack
        player1.update("attack", player1_movement, player2, keys, blocks)
    else:
        player1.update("neutral", player1_movement, player2, keys, blocks)

    # Input handling for player2
    player2_movement = (0, 0)
    if keys[pygame.K_LEFT]:  # Move left (mirrored)
        player2_movement = (3, 0)
        player2.direction = 1
        mustache.direction = -1
    if keys[pygame.K_RIGHT]:  # Move right (mirrored)
        player2_movement = (-3, 0)
        player2.direction = -1
        mustache.direction = 1

    if keys[pygame.K_f]:  # Block (mirrored)
        player2.update("block", player2_movement, player1, keys, blocks)
    elif keys[pygame.K_SPACE]:  # Attack (mirrored)
        player2.update("attack", player2_movement, player1, keys, blocks)
    else:
        player2.update("neutral", player2_movement, player1, keys, blocks)

    # Draw everything
    ground.draw(screen)
    player1.draw(screen)
    player2.draw(screen)

    if player2.lives > 0:
        mustache.draw(screen, player2.x + 25, player2.y + 40)

    for block in blocks:
        block.draw(screen)

    # Update display and tick
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()