# This is a tank game where there are 3 levels red circle is a landmine
# After killing 5 enemies level upgrade to 1 and similarly same in level 2 and at last in level 3 big tanks appear that detroy by 3 bullets
# If player is unable to kill the enemy tank then health of player tank decrease by 10 
# Finally after killing 2 big tanks at level 3 the game is over.. 
# for firing - space key.. To move tank- right, left, up and down key..
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Battle")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)

# Player tank
player_x = screen_width // 2
player_y = screen_height - 60
player_width = 40
player_height = 30
player_speed = 3
player_health = 100

# Enemy tanks
enemy_width = 30
enemy_height = 20
enemy_speed = 2
enemy_list = []
enemy_spawn_timer = 0
enemy_spawn_delay = 1000  # milliseconds

# Projectiles
projectile_width = 5
projectile_height = 10
projectile_speed = 10
projectiles = []

# Landmines
landmine_radius = 15
landmines = []
landmine_spawn_timer = 0
landmine_spawn_delay = 5000  # milliseconds

# Health packs
health_pack_size = 20
health_packs = []
health_pack_spawn_timer = 0
health_pack_spawn_delay = 8000  # milliseconds

# Level and score
level = 1
score = 0
level_up_threshold = 5  # Number of enemies to destroy to level up
level_3_kills = 0  # Track level 3 enemy kills

# Background and sounds
background_image = pygame.image.load(
    r"C:\Users\subed\OneDrive\Documents\hit137 CAS147 Ass3\background.png"
)  # Replace with your actual background image path
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
shoot_sound = pygame.mixer.Sound(r"C:\Users\subed\OneDrive\Documents\hit137 CAS147 Ass3\shoot.wav")
explosion_sound = pygame.mixer.Sound(r"C:\Users\subed\OneDrive\Documents\hit137 CAS147 Ass3\explosion.wav")
background_music = pygame.mixer.music.load(r"C:\Users\subed\OneDrive\Documents\hit137 CAS147 Ass3\backgroung_music.mp3")  
pygame.mixer.music.play(-1)  # Loop the background music

# --- Obstacles ---
obstacles = [
    pygame.Rect(100, 200, 80, 30),
    pygame.Rect(250, 350, 50, 100),
    pygame.Rect(50, 450, 100, 40),
]  # Example obstacles

# --- Classes ---

class Tank:
    def __init__(self, x, y, width, height, color, speed, health, level=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.health = health
        self.level = level
        self.shoot_timer = 0
        self.shoot_delay = 2000  # milliseconds

    def draw(self):
        tank_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, tank_rect)
        turret_x = self.x + self.width // 2
        turret_y = self.y - 10
        pygame.draw.circle(screen, self.color, (turret_x, turret_y), 5)

    def shoot(self):
        self.shoot_timer += clock.get_time()
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            projectile_x = self.x + self.width // 2 - projectile_width // 2
            projectile_y = self.y - projectile_height  # Adjust for enemy
            projectiles.append([projectile_x, projectile_y, "enemy"])

class HealthPack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(r"C:\Users\subed\OneDrive\Documents\hit137 CAS147 Ass3\health pack.png")  # Load health pack image

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Create player tank
player = Tank(player_x, player_y, player_width, player_height, blue, player_speed, player_health)

# --- Functions ---

def create_enemy():
    x = random.randint(0, screen_width - enemy_width)
    y = -enemy_height
    if level < 3:
        health = 1  # Level 1 and 2 tanks have 1 health
    else:
        health = 3  # Level 3 tanks have 3 health
    # Increased size for level 3 tanks
    enemy_list.append(Tank(x, y, 50 if level == 3 else enemy_width, 40 if level == 3 else enemy_height,
                            black if level == 3 else red, enemy_speed, health, level))

def create_landmine():
    x = random.randint(landmine_radius, screen_width - landmine_radius)
    y = -landmine_radius
    landmines.append([x, y])

def create_health_pack():
    x = random.randint(health_pack_size, screen_width - health_pack_size)
    y = -health_pack_size
    health_packs.append(HealthPack(x, y))  # Create HealthPack object

def display_text(text, x, y, size=20, color=black):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Game loop
running = True
game_won = False  # Flag to indicate if the game is won
clock = pygame.time.Clock()
explosions = []  # List to store explosion data
explosion_duration = 10  # Adjust as needed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile_x = player.x + player.width // 2 - projectile_width // 2
                projectile_y = player.y
                projectiles.append([projectile_x, projectile_y, "player"])
                shoot_sound.play()  # Play shoot sound for player

    if not game_won:  # Only update game elements if game is not won
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player.speed
        if keys[pygame.K_RIGHT] and player.x < screen_width - player.width:
            player.x += player.speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player.speed
        if keys[pygame.K_DOWN] and player.y < screen_height - player.height:
            player.y += player.speed

# Enemy tank spawning and movement
        enemy_spawn_timer += clock.get_time()
        if enemy_spawn_timer >= enemy_spawn_delay:
            enemy_spawn_timer = 0
            create_enemy()

        for enemy in enemy_list:
            enemy.y += enemy_speed
            if random.randint(0, 100) < 5:  # 5% chance to shoot each frame
                enemy.shoot()
            if enemy.y > screen_height:
                enemy_list.remove(enemy)
                player_health -= 10

        # Landmine spawning
        landmine_spawn_timer += clock.get_time()
        if landmine_spawn_timer >= landmine_spawn_delay:
            landmine_spawn_timer = 0
            create_landmine()

        # Health pack spawning
        health_pack_spawn_timer += clock.get_time()
        if health_pack_spawn_timer >= health_pack_spawn_delay:
            health_pack_spawn_timer = 0
            create_health_pack()

        # Move projectiles
        for projectile in projectiles[:]:
            if projectile[2] == "player":
                projectile[1] -= projectile_speed
            else:  # Enemy projectile
                projectile[1] += projectile_speed  # Move down
            if projectile[1] < 0 or projectile[1] > screen_height:
                projectiles.remove(projectile)

        # Move landmines
        for landmine in landmines:
            landmine[1] += enemy_speed // 2
            if landmine[1] > screen_height:
                landmines.remove(landmine)

        # Move health packs
        for health_pack in health_packs:
            health_pack.y += enemy_speed // 2
            if health_pack.y > screen_height:
                health_packs.remove(health_pack)

        # Collision detection
        # - Projectiles and enemies
        for projectile in projectiles[:]:
            for enemy in enemy_list[:]:
                if pygame.Rect(
                    projectile[0], projectile[1], projectile_width, projectile_height
                ).colliderect(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                    projectiles.remove(projectile)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        explosion_sound.play()  # Play explosion sound
                        explosions.append([enemy.x, enemy.y, 0])  # Add explosion at enemy position
                        enemy_list.remove(enemy)
                        score += 1
                        if enemy.level == 3:
                            level_3_kills += 1
                        if score % level_up_threshold == 0:
                            level += 1
                            if level > 3:
                                level = 3
                            enemy_speed += 1
                            enemy_spawn_delay = max(200, enemy_spawn_delay - 100)
                        break

        # - Player and landmines
        for landmine in landmines[:]:
            if pygame.Rect(player.x, player.y, player.width, player.height).colliderect(
                pygame.Rect(
                    landmine[0] - landmine_radius,
                    landmine[1] - landmine_radius,
                    2 * landmine_radius,
                    2 * landmine_radius,
                )
            ):
                landmines.remove(landmine)
                player_health -= 10

        # - Player and health packs
        for health_pack in health_packs[:]:
            if pygame.Rect(player.x, player.y, player.width, player.height).colliderect(
                pygame.Rect(
                    health_pack.x, health_pack.y, health_pack_size, health_pack_size
                )
            ):
                health_packs.remove(health_pack)
                player_health = min(100, player_health + 20)

        # Update explosions
        for explosion in explosions[:]:
            explosion[2] += 1  # Increment the explosion timer/frame
            if explosion[2] >= explosion_duration:  # Adjust duration as needed
                explosions.remove(explosion)

    # Drawing
    screen.blit(background_image, (0, 0))  # Draw the background

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, gray, obstacle)

    # Draw player tank
    player.draw()

    # Draw enemy tanks
    for enemy in enemy_list:
        enemy.draw()

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.rect(screen, black, (projectile[0], projectile[1], projectile_width, projectile_height))

    # Draw landmines
    for landmine in landmines:
        pygame.draw.circle(screen, red, (landmine[0], landmine[1]), landmine_radius)

    # Draw health packs
    for health_pack in health_packs:
        health_pack.draw()  # Call the draw method of HealthPack object


    # Display score and health
    display_text(f"Score: {score}", 30, 30)
    display_text(f"Health: {player_health}", screen_width - 80, 30)
    display_text(f"Level: {level}", screen_width // 2, 30)

    # Game Over conditions
    if player_health <= 0:
        display_text("Game Over", screen_width // 2, screen_height // 2, size=40, color=red)
        running = False  # End the game if player health is 0
    elif level_3_kills >= 2:
        display_text("You Win!", screen_width // 2, screen_height // 2, size=40, color=green)
        game_won = True  # Set the game_won flag to True

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit() 