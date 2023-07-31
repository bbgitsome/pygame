import pygame
from gameObject import GameObject
from bullet import Bullet

class Player(GameObject):
    def __init__(self, x, y, width, height, image_path, speed):
        super().__init__(x, y, width, height, image_path)

        self.speed = speed
        self.bullets = []
        self.bullet_speed = 10

    def move(self, direction, x_direction):
        self.y += (direction * self.speed)
        self.x += (x_direction * self.speed)

    def shoot(self):
        bullet = Bullet(self.x + self.width // 2, self.y, 5, 10, self.bullet_speed, 'assets/bullet.png')
        self.bullets.append(bullet)