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

        self.reset_map()
    
    def reset_map(self):
        self.player = Player(365, 725, 65, 74, 'assets/player.png', 10, self.game_window)
        speed = 5 + (self.level * 5)

        if self.level == 4.0:
            self.enemies = [Enemy(0,580,50,50, 'assets/blob.png', speed),
                        Enemy(390,440,50,50, 'assets/blob.png', speed),
                        Enemy(0,300,50,50, 'assets/blob.png', speed),
                        Enemy(390,160,50,50, 'assets/blob.png', speed)]
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

    def draw_objects(self):
        self.game_window.fill(self.bg_color)
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.treasure.image, (self.treasure.x, self.treasure.y))
        self.game_window.blit(self.weapon.image, (self.weapon.x, self.weapon.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))
        for bullet in self.player.bullets:
            self.game_window.blit(bullet.image, (bullet.x, bullet.y))
        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x, enemy.y))
            enemy.draw_health_bar(self.game_window)

        # Display level label at the top left
        font_path = "font/DePixelHalbfett.ttf"
        font = pygame.font.Font(font_path, 36) 
        level_text = f"Level {int(self.level)}"  # Convert level to integer and format the text
        label_surface = font.render(level_text, True, (255, 255, 255))  # Set the color for the level label text
        self.game_window.blit(label_surface, (10, 10))  # Set the position of the label on the screen

        # Draw the hearts (player lives)
        self.draw_hearts()

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
        if self.detect_collisions(self.player, self.treasure):
            self.level += 1.0
            self.reset_map()
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
                # Update enemy health when hit by a bullet
                if isinstance(object_1, Bullet):
                    object_2.receive_damage(25)  # Reduce enemy health by 25

                    # If enemy health is 0 or less, remove the enemy from the game
                    if object_2.health <= 0:
                        self.enemies.remove(object_2)
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
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_direction = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_player_direction = 0
            
            #Execute logic
            self.move_objects(player_direction, x_player_direction)

            # Check bullet-enemy collisions and remove dead enemies
            for bullet in self.player.bullets[:]:
                for enemy in self.enemies[:]:
                    if bullet.check_collision(enemy):
                        self.player.bullets.remove(bullet)
                        enemy.receive_damage(20)  # Reduce enemy health by 25
                        if enemy.is_dead():
                            self.enemies.remove(enemy)

            #Update display
            self.draw_objects()

            # Detect collisions
            if self.check_if_collided():
                if self.player_lives == 0:
                    self.level = 1.0
                    self.reset_map()    
                else:
                    self.player = Player(365, 725, 65, 74, 'assets/player.png', 10, self.game_window)        

            self.clock.tick(60)
