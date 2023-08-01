import pygame
from gameObject import GameObject
from bullet import Bullet

class Enemy(GameObject):
    def __init__(self, x, y, width, height, image_path, speed):
        super().__init__(x, y, width, height, image_path)

        self.speed = speed
        
        # Add health attributes
        self.max_health = 100
        self.health = self.max_health
        self.health = self.max_health
        self.is_alive = True

        # Add attributes for shooting
        self.can_shoot = False
        self.shoot_delay = 800  # Time in milliseconds (adjust as needed)
        self.last_shot_time = pygame.time.get_ticks()
    
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
    
    def update(self):
        # Check if enough time has passed since the last shot
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.can_shoot = True

    def shoot(self, bullets):
        if self.can_shoot:
            bullet_speed = 5  # Adjust the speed as needed
            bullet_width = 10 # Adjust the width of the bullet
            bullet_height = 10  # Adjust the height of the bullet

            bullet = Bullet(self.x + self.width // 2, self.y + self.height, bullet_width, bullet_height, bullet_speed, 'assets/fire.png', None, is_enemy_bullet=True)
            bullets.append(bullet)

            self.last_shot_time = pygame.time.get_ticks()  # Record the time of the last shot
            self.can_shoot = False  # Reset the flag to prevent immediate shooting