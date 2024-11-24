import pygame
import sys
from player import Player
from ground import Ground

# Initialize Pygame
pygame.init()
pygame.font.init()

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
player2 = Player(600, GROUND_Y - 100, PLAYER_IMAGE_PATH, delay=30, lives=5, direction=-1)  # Delayed input

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player1.lives > 0 and player2.lives > 0:
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
        if keys[pygame.K_RIGHT]:  # Move right (mirrored)
            player2_movement = (-3, 0)
            player2.direction = 1

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

        # Update display and tick
        pygame.display.flip()
        clock.tick(FPS)

    else:
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont('Comic Sans MS', 30)

        if player1.lives <= 0:
            text = font.render("You have been destroyed by your twin enemy", False, (0, 0, 0))
        elif player2.lives <= 0:
            text = font.render("You win!", False, (0, 0, 0))
        else:
            text = font.render("It's a tie", False, (0, 0, 0))

        textRect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, textRect)

        restart = pygame.Rect(200, 400, 150, 75)  # restart
        Quit = pygame.Rect(450, 400, 150, 75)  # quit

        pygame.draw.rect(screen, (255, 0, 0), restart)
        pygame.draw.rect(screen, (255, 0, 0), Quit)

        restart_text = font.render("Restart", False, (0, 0, 0))
        screen.blit(restart_text, restart)

        quit_text = font.render("Quit", False, (0, 0, 0))
        screen.blit(quit_text, Quit)

        pygame.display.flip()

        # wait for quit/restart
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if restart.collidepoint(x, y):  # click restart button
                        player1.lives = 5
                        player2.lives = 5
                        player1.x, player1.y = 100, GROUND_Y - 100
                        player2.x, player2.y = 600, GROUND_Y - 100
                        player1.state = "neutral"
                        player2.state = "neutral"
                        wait = False
                    elif Quit.collidepoint(x, y):  # click quit button
                        wait = False
                        running = False

pygame.quit()
sys.exit()