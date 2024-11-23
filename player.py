import pygame
from collections import deque

class Player:
    def __init__(self, x, y, image_path, delay=0):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.image = self.load_image(image_path)
        self.state = "neutral"  # Current state
        self.state_queue = deque(["neutral"] * (delay + 1))  # Queue for delayed states
        self.movement_queue = deque([(0, 0)] * (delay + 1))  # Queue for delayed movements
        self.lives = 5

    def load_image(self, path):
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error:
            print(f"Failed to load image at {path}, falling back to rectangle.")
            return None

    def update(self, state, movement):
        # Update delayed states
        self.state_queue.append(state)
        self.state = self.state_queue.popleft()

        # Update delayed movement
        self.movement_queue.append(movement)
        dx, dy = self.movement_queue.popleft()
        self.x += dx
        self.y += dy

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

        # Optionally, draw the current state for debugging
        font = pygame.font.Font(None, 36)
        text = font.render(self.state, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 30))