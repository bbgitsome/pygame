import pygame
from gameObject import GameObject

class Enemy(GameObject):
    def __init__(self, x, y, width, height, image_path, speed):
        super().__init__(x, y, width, height, image_path)

        self.speed = speed
        
        # Add health attributes
        self.max_health = 100
        self.health = self.max_health
        self.health = self.max_health
        self.is_alive = True
    
    def move(self, max_width):
        if self.x <= 0:
            self.speed = abs(self.speed)
        elif self.x >= max_width - self.width:
            self.speed = -self.speed
        
        self.x += self.speed
    
    def draw_health_bar(self, game_window):
        # Calculate the width of the health bar based on the current health
        health_width = (self.health / 100) * self.width

        # Determine the color of the health bar based on the health level
        if self.health > 60:
            health_bar_color = (0, 255, 0)  # Green when health > 60%
        elif self.health > 30:
            health_bar_color = (255, 255, 0)  # Yellow when 30% < health <= 60%
        else:
            health_bar_color = (255, 0, 0)  # Red when health <= 30%

        # Draw the health bar rectangle
        health_bar_rect = pygame.Rect(self.x, self.y - 10, health_width, 5)
        pygame.draw.rect(game_window, health_bar_color, health_bar_rect)
    
    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False

    def is_dead(self):
        return not self.is_alive