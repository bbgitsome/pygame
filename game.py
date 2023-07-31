import pygame
from gameObject import GameObject
from player import Player
from enemy import Enemy
from bullet import Bullet

class Game:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.bg_color = (0, 150, 255)

        self.game_window = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.background = GameObject(0, 0, self.width, self.height, 'assets/background.png')

        self.treasure = GameObject(365, 50, 65, 74, 'assets/chest.png')
    
        self.weapon = GameObject(707, 704, 38, 45, 'assets/weapon.png')

        self.level = 1.0

        self.heart_image = pygame.image.load('assets/heart.png')
        self.heart_width = 30
        self.heart_height = self.heart_image.get_height()

        self.weapon_collided = False
        self.bullet_collided = False

        self.enemy_bullets = []

        self.display_weapon_message = True
        self.show_bullet_message = True 

        self.reset_map()
    
    def reset_map(self):
        self.player = Player(365, 725, 65, 74, 'assets/player.png', 10, self.game_window)
        speed = 5 + (self.level * 5)

        if self.level == 4.0:
            self.enemies = [Enemy(390,160,50,50, 'assets/alien.png', 5)]
        elif self.level == 3.0:
            self.enemies = [Enemy(0,580,50,50, 'assets/blob.png', speed),
                        Enemy(390,440,50,50, 'assets/blob.png', speed),
                        Enemy(0,300,50,50, 'assets/blob.png', speed)]
        elif self.level == 2.0:
            self.enemies = [Enemy(0,580,50,50, 'assets/blob.png', speed),
                        Enemy(390,440,50,50, 'assets/blob.png', speed)]
        else:
            self.enemies = [Enemy(0,580,50,50, 'assets/blob.png', speed)]

        # Set the player lives to 3 when the map is reset
        self.player_lives = 3

        # Enable or disable the bullet based on the level
        if self.level >= 4.0:
            self.player.has_bullet = True
        else:
            self.player.has_bullet = False

        self.weapon_collided = False
        self.display_weapon_message = True
        self.show_bullet_message = True 
        self.bullet_collided = False

    def render_text(self, text, font_size, color, x, y):
        font_path = "font/DePixelHalbfett.ttf"
        font = pygame.font.Font(font_path, font_size)
        text_surface = font.render(text, True, color)
        self.game_window.blit(text_surface, (x, y))

    def draw_objects(self):
        self.game_window.fill(self.bg_color)
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.treasure.image, (self.treasure.x, self.treasure.y))
        self.game_window.blit(self.weapon.image, (self.weapon.x, self.weapon.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))
        for bullet in self.player.bullets:
            self.game_window.blit(bullet.image, (bullet.x, bullet.y))

        for bullet in self.enemy_bullets:
            self.game_window.blit(bullet.image, (bullet.x, bullet.y))

        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x, enemy.y))
            enemy.draw_health_bar(self.game_window)

        # Display level label at the top left
        font_path = "font/DePixelHalbfett.ttf"
        font = pygame.font.Font(font_path, 26) 
        level_text = f"Level {int(self.level)}"  # Convert level to integer and format the text
        label_surface = font.render(level_text, True, (255, 255, 255))  # Set the color for the level label text
        self.game_window.blit(label_surface, (10, 10))  # Set the position of the label on the screen

        # Draw the hearts (player lives)
        self.draw_hearts()

        if self.level >= 4.0 and self.display_weapon_message:
            self.render_text("Weapon here!", 15, (255, 255, 255), 640, 680)

        if self.player.has_bullet and self.show_bullet_message:
            self.render_text("Press SPACE to use the weapon.", 15, (255, 255, 255), 230, 650)

        pygame.display.update()

    def draw_hearts(self):
        heart_spacing = 40
        heart_y = 50

        for i in range(self.player_lives):
            heart_x = 10 + i * heart_spacing
            self.game_window.blit(self.heart_image, (heart_x, heart_y))

    def move_objects(self, player_direction, x_player_direction):
        self.player.move(player_direction, x_player_direction)
        for enemy in self.enemies:
            enemy.move(self.width)
        
        # Move the bullets
        for bullet in self.player.bullets:
            bullet.move()

            # Remove the bullet if it goes off-screen
            if bullet.y < 0:
                self.player.bullets.remove(bullet)

    def check_if_collided(self):
        for enemy in self.enemies:
            if self.detect_collisions(self.player, enemy):
                self.player_lives -= 1
                return True
        for bullet in self.enemy_bullets:
            if self.detect_collisions(self.player, bullet):
                self.player_lives -= 1
                self.bullet_collided = True
                self.enemy_bullets.remove(bullet)  # Remove the enemy bullet on collision
                return True
        if self.detect_collisions(self.player, self.treasure):
            self.level += 1.0
            self.reset_map()
            return True
        if self.level >= 4.0 and self.detect_collisions(self.player, self.weapon):
            self.weapon_collided = True  # Set the flag to True when the player collides with the weapon
            self.display_weapon_message = False  # Hide the weapon message
            return True

        return False

    def detect_collisions(self, object_1, object_2):
        rect_1 = pygame.Rect(object_1.x, object_1.y, object_1.width, object_1.height)
        rect_2 = pygame.Rect(object_2.x, object_2.y, object_2.width, object_2.height)

        if rect_1.colliderect(rect_2):
            offset_x = object_2.x - object_1.x
            offset_y = object_2.y - object_1.y

            # Use masks to check for precise pixel-perfect collision
            if object_1.mask.overlap(object_2.mask, (offset_x, offset_y)):
                return True
        
        return False

    def run_game_loop(self):

        player_direction = 0
        x_player_direction = 0

        while True:
            #Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_direction = -1
                    elif event.key == pygame.K_DOWN:
                        player_direction = 1
                    elif event.key == pygame.K_LEFT:
                        x_player_direction = -1
                    elif event.key == pygame.K_RIGHT:
                        x_player_direction = 1
                    
                    # Add shooting event
                    elif event.key == pygame.K_SPACE:
                        self.player.shoot()
                        self.show_bullet_message = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_direction = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_player_direction = 0
            
            #Execute logic
            self.move_objects(player_direction, x_player_direction)

            # Update enemies before shooting
            for enemy in self.enemies:
                enemy.update()

            # Check bullet-enemy collisions and remove dead enemies
            for bullet in self.player.bullets[:]:
                for enemy in self.enemies[:]:
                    if bullet.check_collision(enemy):
                        self.player.bullets.remove(bullet)
                        enemy.receive_damage(1)  # Reduce enemy health
                        if enemy.is_dead():
                            self.enemies.remove(enemy)

            # Enemy shooting logic for level 4
            if self.level >= 4.0:
                for enemy in self.enemies:
                    enemy.shoot(self.enemy_bullets)

            # Move enemy bullets
            for bullet in self.enemy_bullets:
                bullet.move()

                # Remove the bullet if it goes off-screen
                if bullet.y > self.height:
                    self.enemy_bullets.remove(bullet)

            #Update display
            self.draw_objects()

            # Detect collisions
            if self.check_if_collided():
                if self.player_lives == 0:
                    self.level = 1.0
                    self.reset_map()
                else:
                    if not self.bullet_collided and not self.weapon_collided:
                        self.player.x = 365  # Reset the player's x position
                        self.player.y = 725  # Reset the player's y position
                        
                    # Enable the bullet for level 4 and when the player has collided with the weapon
                    self.player.has_bullet = self.level >= 4.0 and self.weapon_collided

            self.clock.tick(60)
