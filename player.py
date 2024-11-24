import pygame
from collections import deque
from attack import Attack

class Player:
    def __init__(self, x, y, delay=0, lives=1, direction=1):
        self.x = x
        self.delay = delay
        self.y = y
        self.final_y = y + 50
        self.width = 100
        self.height = 100
        self.velo = 0
        self.roblox_face = False
        self.previous_state = "neutral"
        self.heart_image = self.load_image("Assets/heart.png")
        self.idle_images = [self.load_image("Assets/idle1.png"),
                            self.load_image("Assets/idle2.png")]
        self.running_images = [self.load_image("Assets/running1.png"),
                               self.load_image("Assets/running2.png"),
                               self.load_image("Assets/running3.png"),
                               self.load_image("Assets/running4.png"),
                               self.load_image("Assets/running5.png"),
                               self.load_image("Assets/running6.png")]
        self.shield_images = [self.load_image("Assets/shield1.png"),
                              self.load_image("Assets/shield2.png"),
                              self.load_image("Assets/shield3.png")]
        self.framecount = 0
        self.state = "neutral"  # Current state
        self.state_queue = deque(["neutral"] * (delay * 2 + 1))  # Queue for delayed states
        self.movement_queue = deque([(0, 0)] * (delay + 1))  # Queue for delayed movements
        self.lives = lives
        self.last_attack_time = 0
        self.attack_cooldown = 500
        self.direction = direction
        self.attack = None  # Store current attack object

    def update(self, state, movement, opponent):
        # Update delayed states
        self.state_queue.append(state)
        self.state = self.state_queue.popleft()
        if self.state != self.previous_state:
            self.framecount = 0
            self.roblox_face = False
            self.previous_state = self.state

        # Update delayed movement
        self.movement_queue.append(movement)
        dx, dy = self.movement_queue.popleft()
        self.velo = dx
        if (self.x + dx > 0) and (self.x + dx < 700):
            self.x += dx
        else:
            self.velo = 0
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
            self.attack = Attack(self.x + b, self.y + 25, a, "Assets/bullets.png")  # Example image path

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
                elif opponent.state == "block":
                    opponent.roblox_face = True

            # Remove attack if out of bounds (optional cleanup)
            if self.attack.x < 0 or self.attack.x > 800:
                self.attack = None

    def get_image(self):
        try:
            # Animation frame rate control
            frame_delay = 20  # Number of game frames to wait before switching animation frames
            if self.framecount % frame_delay == 0:
                if self.lives > 0:
                    if self.state != "block":
                        if self.velo != 0:
                            self.current_frame = self.running_images[
                                (self.framecount // frame_delay) % len(self.running_images)]
                        else:
                            self.current_frame = self.idle_images[(self.framecount // frame_delay) % len(self.idle_images)]
                    else:
                        if self.roblox_face == False:
                            self.current_frame = self.shield_images[(self.framecount // frame_delay) % 2]
                        else:
                            self.current_frame = self.shield_images[2]
                else:
                    self.height = 50
                    self.y = self.final_y
                    self.current_frame = self.load_image("Assets/dead.png")

            self.framecount += 1

            if self.direction == 1:
                return pygame.transform.scale(self.current_frame, (self.width, self.height))
            else:
                return pygame.transform.scale(pygame.transform.flip(self.current_frame, True, False),
                                              (self.width, self.height))

        except pygame.error:
            print(f"Failed to load image, falling back to rectangle.")
            return None

    def load_image(self, path):
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error:
            print(f"Warning: Could not load image at {path}. Using fallback surface.")
            return pygame.Surface((self.width, self.height)).convert()

    def draw(self, screen):
        screen.blit(self.get_image(), (self.x, self.y))

        if self.attack:
            self.attack.draw(screen)
            self.attack.x += self.attack.direction * 5