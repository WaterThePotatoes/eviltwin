import pygame
import sys
from player import Player
from ground import Ground

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GROUND_Y = SCREEN_HEIGHT - 50
FPS = 120

# Paths to assets
PLAYER_IMAGE_PATH = "player.png"  # Replace with your player image path
GROUND_IMAGE_PATH = "ground.jpg"  # Replace with your ground image path

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Delayed Input Game")
clock = pygame.time.Clock()

# Create objects
ground = Ground(GROUND_Y, SCREEN_WIDTH, 50, GROUND_IMAGE_PATH)
player1 = Player(100, GROUND_Y - 100, PLAYER_IMAGE_PATH)
player2 = Player(600, GROUND_Y - 100, PLAYER_IMAGE_PATH, delay=30)  # Delayed input

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
    if keys[pygame.K_RIGHT]:  # Move right
        player1_movement = (3, 0)

    if keys[pygame.K_f]:  # Block
        player1.update("block", player1_movement)
    elif keys[pygame.K_SPACE]:  # Attack
        player1.update("attack", player1_movement)
    else:
        player1.update("neutral", player1_movement)

    # Input handling for player2
    player2_movement = (0, 0)
    if keys[pygame.K_LEFT]:  # Move left (mirrored)
        player2_movement = (3, 0)
    if keys[pygame.K_RIGHT]:  # Move right (mirrored)
        player2_movement = (-3, 0)

    if keys[pygame.K_f]:  # Block (mirrored)
        player2.update("block", player2_movement)
    elif keys[pygame.K_SPACE]:  # Attack (mirrored)
        player2.update("attack", player2_movement)
    else:
        player2.update("neutral", player2_movement)

    # Draw everything
    ground.draw(screen)
    player1.draw(screen)
    player2.draw(screen)

    # Update display and tick
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()