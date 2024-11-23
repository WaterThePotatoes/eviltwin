import pygame
from player import Player

pygame.init()
pygame.font.init()

screenW,screenH = 800, 600
screen = pygame.display.set_mode((screenW,screenH))
clock = pygame.time.Clock()
end = False

over_font = pygame.font.SysFont('Comic Sans MS', 80)

mainloop = True

while mainloop:
    clock.tick(500)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
            exit()
        while end:
            screen.fill((255,0,0))
            game_over = over_font.render("Game Over", False, (255, 255, 255))
            screen.blit(game_over, (100, 150))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                    exit()
                break