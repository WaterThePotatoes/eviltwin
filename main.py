import pygame
import time

pygame.init()
pygame.font.init()

screenW,screenH = 800, 600
screen = pygame.display.set_mode((screenW,screenH))
clock = pygame.time.Clock()
end = False

class Character(object):
    def __init__(self, image, width, height, pos):
        self.image = pygame.image.load(image)
        self.width = width
        self.height = height
        self.x,self.y = pos

    def draw(self):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, (self.x, self.y))

    def Rect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)

class CurrentCharacter(Character):
    def __init__(self, image, width, height, pos):
        self.image = pygame.image.load(image)

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
            screen.fill((0,0,0))
            game_over = over_font.render("Game Over", False, (255, 255, 255))
            screen.blit(game_over, (100, 150))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                    exit()
                break

"""
class CurrentCharacter(Character):
    def __init__(self,name,image,width,height,pos,speed):
        self.name = name
        self.image = pg.image.load(image)
        self.images = [self.image]
        self.width = width
        self.height = height
        self.x,self.y = pos
        self.speed = speed
        self.rect = self.image.get_rect()
        self.th = self.height
        self.tw = self.width

    def Rect(self):
        self.rect = pg.Rect(self.x,self.y,self.tw,self.th)
        return self.rect

    def run(self):
        self.rect = self.Rect()
        if keys[pg.K_LEFT] and self.x > 0+self.width:
            self.x -= self.speed
            for i in self.images[1:]:
                i.x -= self.speed


        if keys[pg.K_RIGHT] and self.x < screenW - self.width:
            self.x += self.speed
            for i in self.images[1:]:
                i.x += self.speed

        if keys[pg.K_UP] and self.y > 0+self.height:
            self.y -= self.speed
            for i in self.images[1:]:
                i.y -= self.speed

        if keys[pg.K_DOWN] and self.y < screenH - self.height:
            self.y += self.speed
            for i in self.images[1:]:
                i.y += self.speed


        for x in collidables:
            if self.rect.colliderect(x.Rect()):
                self.images.append(x)

                self.x = min(self.x, x.x)
                self.y = min(self.y, x.y)
                self.tw = max(self.x + self.width, x.x + x.width) - self.x
                self.th = max(self.y + self.height, x.y + x.height) - self.y


                collidables.remove(x)"""