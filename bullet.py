import pygame
from gameObject import GameObject

class Bullet:
    def __init__(self, x, y, width, height, speed, image_path, game_window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.image.load(image_path).convert_alpha()
        self.game_window = game_window

    def move(self):
        self.y -= self.speed

    def check_collision(self, enemy):
        bullet_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

        if bullet_rect.colliderect(enemy_rect):
            enemy.receive_damage(25)  # Reduce enemy health by 25
            return True

        return False
