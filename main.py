import pygame
import sys
from player import Player
from ground import Ground
from mustache import Mustache

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GROUND_Y = SCREEN_HEIGHT - 50
FPS = 120

GROUND_IMAGE_PATH = "ground.jpg"  # Replace with your ground image path

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Evil Twins")
clock = pygame.time.Clock()

# Create objects
ground = Ground(GROUND_Y, SCREEN_WIDTH, 50, GROUND_IMAGE_PATH)
player1 = Player(100, GROUND_Y - 100)
player2 = Player(600, GROUND_Y - 100, delay=30, lives=5, direction=-1)  # Delayed input
mustache = Mustache()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black
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
        player1.update("block", player1_movement, player2)
    elif keys[pygame.K_SPACE]:  # Attack
        player1.update("attack", player1_movement, player2)
    else:
        player1.update("neutral", player1_movement, player2)

    # Input handling for player2
    player2_movement = (0, 0)
    if keys[pygame.K_LEFT]:  # Move left (mirrored)
        player2_movement = (3, 0)
        player2.direction = -1
        mustache.direction = -1
    if keys[pygame.K_RIGHT]:  # Move right (mirrored)
        player2_movement = (-3, 0)
        player2.direction = 1
        mustache.direction = 1

    if keys[pygame.K_f]:  # Block (mirrored)
        player2.update("block", player2_movement, player1)
    elif keys[pygame.K_SPACE]:  # Attack (mirrored)
        player2.update("attack", player2_movement, player1)
    else:
        player2.update("neutral", player2_movement, player1)

    # Draw everything
    ground.draw(screen)
    player1.draw(screen)
    player2.draw(screen)
    mustache.draw(screen, player2.x + 25, player2.y + 40)

    # Update display and tick
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()