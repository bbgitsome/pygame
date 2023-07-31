import pygame
from gameObject import GameObject

class Bullet:
    def __init__(self, x, y, width, height, speed, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.image.load(image_path).convert_alpha()

    def move(self):
        self.y -= self.speed
