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
        self.state_queue = deque(["neutral"] * (delay*3 + 1))  # Queue for delayed states
        self.movement_queue = deque([(0, 0)] * (delay + 1))  # Queue for delayed movements
        self.lives = 5
        self.last_attack_time = 0
        self.attack_cooldown = 500

    def load_image(self, path):
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error:
            print(f"Failed to load image at {path}, falling back to rectangle.")
            return None

    def update(self, state, movement, Player):
        # Update delayed states
        self.state_queue.append(state)
        self.state = self.state_queue.popleft()

        # Update delayed movement
        self.movement_queue.append(movement)
        dx, dy = self.movement_queue.popleft()
        if (self.x + dx > 0) and (self.x + dx < 700):
            self.x += dx
        self.y += dy

        # Current time in milliseconds
        current_time = pygame.time.get_ticks()

        # Attack Logic: Check if the cooldown has elapsed
        if self.state == "attack" and current_time - self.last_attack_time >= self.attack_cooldown:
            # Check for collision with the other player's attack
            if (self.x + 100 >= Player.x) and (self.x <= Player.x + 100):
                if Player.state == "attack" and self.state != "block":
                    self.lives -= 1  # Player 1 takes damage from Player 2's attack
                if self.state == "attack" and Player.state != "block":
                    Player.lives -= 1  # Player 2 takes damage from Player 1's attack

            # Update the last attack time
            self.last_attack_time = current_time



    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

        # Optionally, draw the current state for debugging
        font = pygame.font.Font(None, 36)
        text = font.render(self.state + str(self.lives), True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 30))