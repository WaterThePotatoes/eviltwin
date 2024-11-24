import pygame
from collections import deque
from attack import Attack

class Player:
    def __init__(self, x, y, image_path, delay=0, lives=1, direction=1):
        self.x = x
        self.delay = delay
        self.y = y
        self.width = 100
        self.height = 100
        self.image = self.load_image(image_path)
        self.state = "neutral"  # Current state
        self.state_queue = deque(["neutral"] * (delay * 2 + 1))  # Queue for delayed states
        self.movement_queue = deque([(0, 0)] * (delay + 1))  # Queue for delayed movements
        self.lives = lives
        self.last_attack_time = 0
        self.attack_cooldown = 500
        self.direction = direction
        self.attack = None  # Store current attack object

    def load_image(self, path):
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error:
            print(f"Failed to load image at {path}, falling back to rectangle.")
            return None

    def update(self, state, movement, opponent):
        # Update delayed states
        self.state_queue.append(state)
        self.state = self.state_queue.popleft()

        # Update delayed movement
        self.movement_queue.append(movement)
        dx, dy = self.movement_queue.popleft()
        if (self.x + dx > 0) and (self.x + dx < 700):
            self.x += dx
        self.y += dy

        # Attack Logic: Check if the cooldown has elapsed
        current_time = pygame.time.get_ticks()
        if self.state == "attack" and current_time - self.last_attack_time >= self.attack_cooldown:
            # Create the attack object
            if self.delay == 0:
                a = 1 * self.direction
                b = 100 * self.direction
            else:
                a = -1 * self.direction
                b = -100 * self.direction
            self.attack = Attack(self.x + b, self.y + 25, a, "attack_image.png")  # Example image path

        # Check for collision only if an attack exists
        # Check for collision only if an attack exists
        if self.attack:
            # Update attack position
            self.attack.x += self.attack.direction*.5

            # Define attack range
            if self.attack.direction > 0:  # Moving to the right
                attack_start = self.attack.x
                attack_end = self.attack.x + self.attack.width
            else:  # Moving to the left
                attack_start = self.attack.x - self.attack.width
                attack_end = self.attack.x

            # Define opponent range
            opponent_start = opponent.x
            opponent_end = opponent.x + opponent.width

            # Check for overlap
            if attack_end >= opponent_start and attack_start <= opponent_end:
                print(
                    f"Collision detected: Attack ({attack_start}, {attack_end}) vs Opponent ({opponent_start}, {opponent_end})")
                current_time = pygame.time.get_ticks()
                if opponent.state != "block" and current_time - self.last_attack_time >= self.attack_cooldown:
                    opponent.lives -= 1
                    self.last_attack_time = current_time

            # Remove attack if out of bounds (optional cleanup)
            if self.attack.x < 0 or self.attack.x > 800:
                self.attack = None

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

        # Optionally, draw the current state for debugging
        font = pygame.font.Font(None, 36)
        text = font.render(f"{self.state} {self.lives}", True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 30))

        if self.attack:
            self.attack.draw(screen)
            self.attack.x += self.attack.direction * 5