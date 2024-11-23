import pygame
from ground import Ground
class Player():
    def __init__(self, startingPos: list[int, int], enemy: False):
        self.startingPos = startingPos
