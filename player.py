import pygame
from gameObject import GameObject
from bullet import Bullet

class Player(GameObject):
    def __init__(self, x, y, width, height, image_path, speed, game_window):
        super().__init__(x, y, width, height, image_path)

        self.speed = speed
        self.bullets = []
        self.bullet_speed = 10
        self.game_window = game_window
        self.has_bullet = False  # New attribute to keep track of whether the player has a bullet or not

    def move(self, direction, x_direction):
        self.y += (direction * self.speed)
        self.x += (x_direction * self.speed)

    def shoot(self):
        if self.has_bullet:
            bullet = Bullet(self.x + self.width // 2, self.y, 5, 10, self.bullet_speed, 'assets/blue.png', self.game_window)
            self.bullets.append(bullet)