import pygame
import sys
import random
import os
import math
from sprites import Fruit, Basket, Conveyor, Button, ParticleSystem, Background
from sound_effects import SoundEffects
from music import BackgroundMusic

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "NEON FRUIT CATCHER"

# Enhanced colors (neon retro style)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_RED = (255, 60, 120)
NEON_GREEN = (60, 255, 120)
NEON_BLUE = (60, 120, 255)
NEON_YELLOW = (255, 255, 60)
NEON_ORANGE = (255, 150, 60)
NEON_PURPLE = (200, 60, 255)
NEON_PINK = (255, 100, 200)
NEON_CYAN = (60, 255, 255)

class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        
        # Load sound effects
        self.sound_fx = SoundEffects()
        
        # Load background music
        self.music = BackgroundMusic()
        self.music.fade_in(2000)  # Fade in over 2 seconds
        
        # Game state
        self.running = True
        self.current_screen = "home"  # "home", "game", "info"
        self.best_score = 0
        
        # Create home screen elements
        self.create_home_screen()
        
        # Font for text - use custom pixel font if available
        try:
            font_path = os.path.join("assets", "fonts", "pixel.ttf")
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 36)
                self.title_font = pygame.font.Font(font_path, 72)
            else:
                self.font = pygame.font.Font(None, 36)
                self.title_font = pygame.font.Font(None, 72)
        except:
            self.font = pygame.font.Font(None, 36)
            self.title_font = pygame.font.Font(None, 72)
        
        # Create particle system
        self.particles = ParticleSystem()
        
        # Create background
        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Preload fruit images for decorative purposes
        self.fruit_types = ["apple", "banana", "orange", "star_fruit", "blueberry"]
        self.decorative_fruits = []
        self.create_decorative_fruits()
    
    def create_decorative_fruits(self):
        """Create decorative fruits for the home screen with bouncing behavior"""
        self.decorative_fruits = []
        positions = [
            (150, 150),  # Top left
            (650, 150),  # Top right
            (150, 450),  # Bottom left
            (650, 450)   # Bottom right
        ]
        
        # Use specific fruit types for each position
        fruit_types = ["apple", "banana", "orange", "star_fruit"]
        
        for i, pos in enumerate(positions):
            fruit_type = fruit_types[i]
            fruit = Fruit(pos[0], pos[1], fruit_type, "basket", 0)
            
            # Add bounce properties
            fruit.bounce_speed_x = random.uniform(-2, 2)
            fruit.bounce_speed_y = random.uniform(-2, 2)
            fruit.bounce_amplitude = random.uniform(0.5, 1.5)
            fruit.bounce_offset = random.uniform(0, math.pi * 2)
            fruit.original_pos = pos
            
            self.decorative_fruits.append(fruit)
    
    def create_home_screen(self):
        # Create normal mode button
        self.start_button = Button(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 40,
            200, 60,
            "NORMAL MODE",
            NEON_GREEN
        )
        
        # Create unlimited mode button
        self.unlimited_button = Button(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 40,
            200, 60,
            "UNLIMITED",
            NEON_PURPLE
        )
        
        # Create info button
        self.info_button = Button(
            SCREEN_WIDTH - 30,
            30,
            40, 40,
            "i",
            NEON_BLUE
        )
        
        # Create mute button with speaker icon
        self.mute_button = Button(
            SCREEN_WIDTH - 30,
            80,
            40, 40,
            "speaker",
            NEON_RED,
            is_icon=True
        )
        
        # Sound state
        self.muted = False
    
    def start_new_game(self, mode="normal"):
        # Game state
        self.current_screen = "game"
        self.game_over = False
        self.score = 0
        self.lives = 3
        self.level = 1
        self.fruit_speed = 2.5  # Reduced initial speed
        self.game_mode = mode
        
        # Timer for unlimited mode
        self.unlimited_timer = 55 * 1000  # 55 seconds in milliseconds
        self.timer_start_time = pygame.time.get_ticks()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.baskets = pygame.sprite.Group()
        
        # Create single basket
        self.basket = Basket(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, "basket")
        self.all_sprites.add(self.basket)
        self.baskets.add(self.basket)
        
        # Game timers
        self.fruit_spawn_timer = 0
        self.fruit_spawn_delay = 2000  # Increased delay for easier gameplay
        self.next_fruit_spawn = random.randint(1000, 2000)  # More predictable timing
        
        # Bomb timer
        self.bomb_spawn_timer = 0
        self.bomb_spawn_delay = 1500  # Increased delay for bombs
        self.next_bomb_spawn = random.randint(1000, 2000)  # More predictable timing
        
        # Game start time
        self.game_start_time = pygame.time.get_ticks()
        
        # Fruit spawn pattern variables
        self.fruit_pattern = "single"  # Start with single fruit
        self.pattern_change_timer = 0
        self.pattern_change_delay = 15000  # Change pattern less frequently (15 seconds)
        
        # Milestone tracking
        self.last_milestone = 0
        self.milestone_increment = 1000
        self.speed_boost_milestone = 2000  # Special milestone for speed boost
        self.speed_boosted = False
        
        # Fruit count progression
        if mode == "unlimited":
            self.fruits_per_drop = 8  # Start with more fruits in unlimited mode
            self.max_fruits_per_drop = 15  # Allow more fruits in unlimited mode
            self.fruit_spawn_delay = 1200  # Faster spawning in unlimited mode
        else:
            self.fruits_per_drop = 1  # Start with 1 fruit at a time in normal mode
            self.max_fruits_per_drop = 6
        
        # Clear particles
        self.particles = ParticleSystem()
    
    def spawn_fruit(self, x=None, speed_modifier=1.0):
        # Fruit types without bombs (bombs are spawned separately)
        fruit_types = ["apple", "banana", "orange", "star_fruit", "blueberry"]
        weights = [25, 25, 25, 15, 15]
        
        # Randomly select a fruit type based on weights
        fruit_type = random.choices(fruit_types, weights=weights, k=1)[0]
        
        # Create the fruit at a random x position at the top of the screen if not specified
        if x is None:
            x = random.randint(SCREEN_WIDTH // 6, 5 * SCREEN_WIDTH // 6)
        
        # Add minimal randomness to the speed for more predictable gameplay
        speed = self.fruit_speed * speed_modifier * random.uniform(0.9, 1.1)
        
        new_fruit = Fruit(x, 0, fruit_type, "basket", speed)
        self.all_sprites.add(new_fruit)
        self.fruits.add(new_fruit)
        return new_fruit
    
    def spawn_bomb(self, x=None):
        # Create a bomb at a random x position at the top of the screen if not specified
        if x is None:
            x = random.randint(SCREEN_WIDTH // 6, 5 * SCREEN_WIDTH // 6)
        
        # Slightly randomize bomb speed
        bomb_speed = self.fruit_speed * 1.1 * random.uniform(0.95, 1.05)  # Less variation
        
        new_bomb = Fruit(x, 0, "bomb", "basket", bomb_speed)
        self.all_sprites.add(new_bomb)
        self.fruits.add(new_bomb)
        
        # Play spawn sound for bombs (with 50% chance to reduce sound spam)
        if random.random() > 0.5:
            self.sound_fx.play("spawn_bomb")
        
        return new_bomb
    
    def spawn_fruit_pattern(self, pattern_type="single"):
        """Spawn fruits in different patterns"""
        # Limit the number of fruits based on current progression
        max_fruits = min(self.fruits_per_drop, self.max_fruits_per_drop)
        
        # In unlimited mode, add some randomness to the number of fruits
        if self.game_mode == "unlimited" and random.random() < 0.3:  # 30% chance for bonus fruits
            max_fruits += random.randint(1, 3)  # Add 1-3 extra fruits randomly
        
        if pattern_type == "single" or max_fruits == 1:
            # Just spawn a single fruit
            x = random.randint(SCREEN_WIDTH // 6, 5 * SCREEN_WIDTH // 6)
            self.spawn_fruit(x)
            
        elif pattern_type == "wave" and max_fruits >= 3:
            # Spawn fruits in a wave pattern (simplified)
            base_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
            for i in range(min(max_fruits, 6)):  # Maximum 6 fruits in wave pattern
                x = (base_x + i * 80) % SCREEN_WIDTH  # Increased spacing
                self.spawn_fruit(x)
        
        elif pattern_type == "cluster" and max_fruits >= 2:
            # Spawn a tight cluster of fruits (simplified)
            center_x = random.randint(SCREEN_WIDTH // 3, 2 * SCREEN_WIDTH // 3)
            for _ in range(min(max_fruits, 5)):  # Maximum 5 fruits in cluster
                x = center_x + random.randint(-60, 60)
                x = max(50, min(SCREEN_WIDTH - 50, x))  # Keep within screen bounds
                self.spawn_fruit(x)
        
        elif pattern_type == "random":
            # Spawn random fruits (simplified)
            num_fruits = random.randint(1, max_fruits)
            for _ in range(num_fruits):
                self.spawn_fruit()
        
        elif pattern_type == "alternating" and max_fruits >= 2:
            # Spawn fruits alternating from left to right (simplified)
            sections = min(5, max_fruits)  # Maximum 5 sections
            section_width = SCREEN_WIDTH / sections
            for i in range(sections):
                if i % 2 == 0 or max_fruits > 3:  # Only spawn in alternating sections unless we have enough fruits
                    x = i * section_width + random.randint(0, int(section_width))
                    self.spawn_fruit(x)
        
        elif pattern_type == "corners" and max_fruits >= 2:
            # Spawn fruits at the edges and middle (simplified)
            positions = [SCREEN_WIDTH // 6, SCREEN_WIDTH // 3, SCREEN_WIDTH // 2, 
                        2 * SCREEN_WIDTH // 3, 5 * SCREEN_WIDTH // 6]
            positions = positions[:max_fruits]  # Limit based on max fruits
            for x in positions:
                self.spawn_fruit(x)
        
        else:
            # Default to single fruit if pattern doesn't match or not enough fruits
            x = random.randint(SCREEN_WIDTH // 6, 5 * SCREEN_WIDTH // 6)
            self.spawn_fruit(x)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "game":
                        self.current_screen = "home"
                    else:
                        self.running = False
                
                # Mute/unmute with M key
                if event.key == pygame.K_m:
                    self.toggle_mute()
            
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Add crackle effect at mouse position for any click
                self.particles.add_crackle(event.pos[0], event.pos[1])
                
                if self.current_screen == "home" or self.current_screen == "game":
                    # Check if mute button was clicked
                    if self.mute_button.is_clicked(event.pos):
                        self.toggle_mute()
                
                if self.current_screen == "home":
                    # Check if start button was clicked
                    if self.start_button.is_clicked(event.pos):
                        self.sound_fx.play("correct")
                        # Add particles at click position
                        self.particles.add_particles(event.pos[0], event.pos[1], NEON_GREEN, 20)
                        self.start_new_game(mode="normal")
                    
                    # Check if unlimited button was clicked
                    if self.unlimited_button.is_clicked(event.pos):
                        self.sound_fx.play("correct")
                        # Add particles at click position
                        self.particles.add_particles(event.pos[0], event.pos[1], NEON_PURPLE, 20)
                        self.start_new_game(mode="unlimited")
                    
                    # Check if info button was clicked
                    if self.info_button.is_clicked(event.pos):
                        self.sound_fx.play("correct")
                        # Add particles at click position
                        self.particles.add_particles(event.pos[0], event.pos[1], NEON_BLUE, 20)
                        self.current_screen = "info"
                
                elif self.current_screen == "info":
                    # Any click returns to home screen
                    self.sound_fx.play("correct")
                    # Add particles at click position
                    self.particles.add_particles(event.pos[0], event.pos[1], NEON_BLUE, 20)
                    self.current_screen = "home"
            
            # Handle music fade events
            elif event.type == pygame.USEREVENT + 1:
                self.music.update_fade()
            elif event.type == pygame.USEREVENT + 2:
                self.music.update_fade_out()
        
        # Check for continuous key presses for basket movement (only in game screen)
        if self.current_screen == "game":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:  # A key for left movement
                self.basket.move_left()
            if keys[pygame.K_d]:  # D key for right movement
                self.basket.move_right()
    
    def toggle_mute(self):
        """Toggle mute/unmute for all sounds"""
        self.muted = not self.muted
        
        if self.muted:
            self.sound_fx.set_volume(0)
            self.music.set_volume(0)
            self.mute_button.text = "speaker-muted"
        else:
            self.sound_fx.set_volume(0.4)
            self.music.set_volume(0.4)
            self.mute_button.text = "speaker"
    
    def update(self):
        # Update background
        self.background.update()
        
        # Update particles
        self.particles.update()
        
        if self.current_screen == "home" or self.current_screen == "info":
            # Update button hover state
            mouse_pos = pygame.mouse.get_pos()
            self.start_button.update(mouse_pos)
            
            # Update info button hover state
            if self.current_screen == "home":
                self.info_button.update(mouse_pos)
                self.unlimited_button.update(mouse_pos)
                self.mute_button.update(mouse_pos)
            
            # Animate and bounce decorative fruits
            current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds for smoother animation
            for fruit in self.decorative_fruits:
                # Basic rotation and pulse animation
                fruit.update()
                
                # Bouncing motion
                if hasattr(fruit, 'original_pos') and hasattr(fruit, 'bounce_speed_x'):
                    # Calculate new position with bouncing effect
                    fruit.rect.centerx = fruit.original_pos[0] + math.sin(current_time * fruit.bounce_speed_x + fruit.bounce_offset) * 50 * fruit.bounce_amplitude
                    fruit.rect.centery = fruit.original_pos[1] + math.cos(current_time * fruit.bounce_speed_y + fruit.bounce_offset) * 30 * fruit.bounce_amplitude
                    
                    # Keep fruits within screen bounds
                    if fruit.rect.left < 0:
                        fruit.rect.left = 0
                        fruit.bounce_speed_x *= -1
                    if fruit.rect.right > SCREEN_WIDTH:
                        fruit.rect.right = SCREEN_WIDTH
                        fruit.bounce_speed_x *= -1
                    if fruit.rect.top < 0:
                        fruit.rect.top = 0
                        fruit.bounce_speed_y *= -1
                    if fruit.rect.bottom > SCREEN_HEIGHT:
                        fruit.rect.bottom = SCREEN_HEIGHT
                        fruit.bounce_speed_y *= -1
            
            return
        
        # Update mute button in game screen
        if self.current_screen == "game":
            mouse_pos = pygame.mouse.get_pos()
            self.mute_button.update(mouse_pos)
        
        if self.game_over:
            # Update best score if current score is higher
            if self.score > self.best_score:
                self.best_score = self.score
            
            # Show game over message briefly, then return to home screen
            current_time = pygame.time.get_ticks()
            if current_time - self.game_over_time > 2000:  # 2 seconds
                self.current_screen = "home"
            return
        
        # Update all sprites
        self.all_sprites.update()
        
        # Check timer for unlimited mode
        if self.game_mode == "unlimited":
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.timer_start_time
            
            # End game when timer runs out
            if elapsed_time >= self.unlimited_timer:
                self.game_over = True
                self.game_over_time = current_time
                self.sound_fx.play("game_over")
                # Add explosion particles
                for _ in range(20):
                    self.particles.add_particles(
                        random.randint(0, SCREEN_WIDTH),
                        random.randint(0, SCREEN_HEIGHT),
                        NEON_YELLOW, 30
                    )
        
        # Check for collisions between fruits and baskets
        for fruit in list(self.fruits):
            # Check if fruit has fallen off the bottom of the screen
            if fruit.rect.top > SCREEN_HEIGHT:
                if fruit.fruit_type != "bomb":  # Only lose a life if it's not a bomb
                    if self.game_mode == "normal":
                        self.lives -= 1
                        self.sound_fx.play("miss")
                        # Add particles where fruit was lost
                        self.particles.add_particles(fruit.rect.centerx, SCREEN_HEIGHT, NEON_RED, 15)
                        if self.lives <= 0:
                            self.game_over = True
                            self.game_over_time = pygame.time.get_ticks()
                            self.sound_fx.play("game_over")
                            # Add explosion particles
                            for _ in range(20):
                                self.particles.add_particles(
                                    random.randint(0, SCREEN_WIDTH),
                                    random.randint(0, SCREEN_HEIGHT),
                                    NEON_RED, 30
                                )
                fruit.kill()
                continue
            
            # Check for collisions with basket
            if pygame.sprite.collide_rect(fruit, self.basket):
                # Handle different fruit types
                if fruit.fruit_type == "bomb":
                    if self.game_mode == "normal":
                        # Game over immediately when bomb is caught in normal mode
                        self.lives = 0
                        self.sound_fx.play("bomb")
                        # Add explosion particles
                        self.particles.add_particles(fruit.rect.centerx, fruit.rect.centery, NEON_RED, 50)
                        
                        self.game_over = True
                        self.game_over_time = pygame.time.get_ticks()
                        self.sound_fx.play("game_over")
                        
                        # Add more explosion particles across the screen
                        for _ in range(30):
                            self.particles.add_particles(
                                random.randint(0, SCREEN_WIDTH),
                                random.randint(0, SCREEN_HEIGHT),
                                NEON_RED, 30
                            )
                    else:
                        # In unlimited mode, bombs just deduct 50 points
                        self.score = max(0, self.score - 50)  # Don't go below 0
                        self.sound_fx.play("wrong")
                        # Add explosion particles
                        self.particles.add_particles(fruit.rect.centerx, fruit.rect.centery, NEON_RED, 30)
                else:
                    # All fruits are good to catch
                    self.score += 100
                    self.sound_fx.play("correct")
                    # Add positive particles
                    if fruit.fruit_type == "apple":
                        color = NEON_RED
                    elif fruit.fruit_type == "banana":
                        color = NEON_YELLOW
                    elif fruit.fruit_type == "orange":
                        color = NEON_ORANGE
                    elif fruit.fruit_type == "star_fruit":
                        color = NEON_YELLOW
                    elif fruit.fruit_type == "blueberry":
                        color = NEON_BLUE
                    else:
                        color = NEON_GREEN
                    
                    self.particles.add_particles(fruit.rect.centerx, fruit.rect.centery, color, 20)
                
                fruit.kill()
        
        # Spawn new fruits with varied patterns (simplified)
        current_time = pygame.time.get_ticks()
        
        # Check if it's time to change the spawn pattern
        if current_time - self.pattern_change_timer > self.pattern_change_delay:
            patterns = ["random", "wave", "cluster", "alternating", "corners"]
            self.fruit_pattern = random.choice(patterns)
            self.pattern_change_timer = current_time
            
            # Add visual effect for pattern change
            pattern_colors = {
                "random": NEON_PURPLE,
                "wave": NEON_BLUE,
                "cluster": NEON_GREEN,
                "alternating": NEON_YELLOW,
                "corners": NEON_ORANGE
            }
            color = pattern_colors.get(self.fruit_pattern, NEON_CYAN)
            
            # Add particles at the top of the screen to indicate pattern change
            for _ in range(20):
                self.particles.add_particles(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, 50),
                    color, 15
                )
        
        # Simplified fruit spawning with more predictable timing
        if current_time - self.fruit_spawn_timer > self.next_fruit_spawn:
            self.spawn_fruit_pattern(self.fruit_pattern)
            self.fruit_spawn_timer = current_time
            # More predictable spawn timing
            self.next_fruit_spawn = random.randint(
                max(1000, self.fruit_spawn_delay - 300),
                self.fruit_spawn_delay + 200
            )
        
        # Simplified bomb spawning with more predictable timing
        if current_time - self.bomb_spawn_timer > self.next_bomb_spawn:
            # 60% chance to spawn a bomb
            if random.random() < 0.6:
                self.spawn_bomb()
            
            self.bomb_spawn_timer = current_time
            
            # More predictable bomb spawn timing
            self.next_bomb_spawn = random.randint(
                max(1000, self.bomb_spawn_delay - 200),
                self.bomb_spawn_delay + 500
            )
        
        # Check for milestone achievements
        if self.score >= self.last_milestone + self.milestone_increment:
            # Player has reached a new milestone
            self.last_milestone = (self.score // self.milestone_increment) * self.milestone_increment
            
            # Increase difficulty slightly
            self.fruit_speed += 0.2
            self.fruit_spawn_delay = max(800, self.fruit_spawn_delay - 100)
            
            # Increase number of fruits per drop (up to max_fruits_per_drop)
            milestone_number = self.last_milestone // self.milestone_increment
            self.fruits_per_drop = min(1 + milestone_number // 2, self.max_fruits_per_drop)
            
            # Update pattern based on fruits_per_drop
            if self.fruits_per_drop == 1:
                self.fruit_pattern = "single"
            elif self.fruits_per_drop == 2:
                patterns = ["random", "cluster"]
                self.fruit_pattern = random.choice(patterns)
            else:
                patterns = ["random", "wave", "cluster", "alternating", "corners"]
                self.fruit_pattern = random.choice(patterns)
            
            # Special speed boost at 2000 points
            if self.last_milestone >= self.speed_boost_milestone and not self.speed_boosted:
                self.speed_boosted = True
                self.fruit_speed += 0.5  # Additional speed boost
                self.fruit_spawn_delay = max(600, self.fruit_spawn_delay - 200)  # Drop faster
                
                # Visual feedback for speed boost
                boost_text = "SPEED BOOST!"
                boost_font = pygame.font.Font(None, 60)
                text_surface = boost_font.render(boost_text, True, NEON_RED)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50))
                self.screen.blit(text_surface, text_rect)
                
                # Add special speed boost particles
                for _ in range(80):
                    self.particles.add_particles(
                        random.randint(0, SCREEN_WIDTH),
                        random.randint(0, SCREEN_HEIGHT),
                        NEON_RED, 25
                    )
            
            # Visual feedback for milestone
            milestone_text = f"{self.last_milestone} POINTS!"
            milestone_font = pygame.font.Font(None, 48)
            text_surface = milestone_font.render(milestone_text, True, NEON_YELLOW)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(text_surface, text_rect)
            
            # Add celebration particles
            for _ in range(50):
                self.particles.add_particles(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 2),
                    NEON_YELLOW, 20
                )
        
        # Increase difficulty over time based on milestones instead of level
        if self.score > self.level * 1000:
            self.level += 1
            
            # Add level up particles
            for _ in range(30):
                self.particles.add_particles(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT // 2),
                    NEON_CYAN, 20
                )
            
            # Add level up particles
            for _ in range(30):
                self.particles.add_particles(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT // 2),
                    NEON_CYAN, 20
                )
    
    def draw_home_screen(self):
        # Draw title with glow effect
        title_text = self.title_font.render("NEON FRUIT CATCHER", True, NEON_CYAN)
        
        # Draw glow effect for title
        glow_surf = pygame.Surface((title_text.get_width() + 20, title_text.get_height() + 20), pygame.SRCALPHA)
        for i in range(10, 0, -2):
            alpha = 20 - i * 2
            pygame.draw.rect(glow_surf, (*NEON_CYAN, alpha), 
                           (10-i, 10-i, title_text.get_width() + i*2, title_text.get_height() + i*2), 
                           border_radius=5)
        
        title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
        title_y = SCREEN_HEIGHT // 4 - title_text.get_height() // 2
        self.screen.blit(glow_surf, (title_x - 10, title_y - 10))
        self.screen.blit(title_text, (title_x, title_y))
        
        # Draw start button
        self.start_button.draw(self.screen)
        
        # Draw unlimited mode button
        self.unlimited_button.draw(self.screen)
        
        # Draw info button
        self.info_button.draw(self.screen)
        
        # Draw mute button
        self.mute_button.draw(self.screen)
        
        # Draw best score at the bottom left corner
        if self.best_score > 0:
            best_score_text = self.font.render(f"BEST SCORE: {self.best_score}", True, NEON_YELLOW)
            
            # Add glow effect for best score
            glow_surf = pygame.Surface((best_score_text.get_width() + 10, best_score_text.get_height() + 10), pygame.SRCALPHA)
            for i in range(5, 0, -1):
                alpha = 15 - i * 2
                pygame.draw.rect(glow_surf, (*NEON_YELLOW, alpha), 
                               (5-i, 5-i, best_score_text.get_width() + i*2, best_score_text.get_height() + i*2), 
                               border_radius=3)
            
            # Position at bottom left with padding
            self.screen.blit(glow_surf, (15 - 5, SCREEN_HEIGHT - 40 - 5))
            self.screen.blit(best_score_text, (15, SCREEN_HEIGHT - 40))
        
        # Draw decorative fruits with effects
        for fruit in self.decorative_fruits:
            fruit.draw_with_effects(self.screen)
    
    def draw_info_screen(self):
        # Draw title with glow effect
        title_text = self.font.render("HOW TO PLAY", True, NEON_YELLOW)
        
        # Draw glow effect for title
        glow_surf = pygame.Surface((title_text.get_width() + 20, title_text.get_height() + 20), pygame.SRCALPHA)
        for i in range(10, 0, -2):
            alpha = 20 - i * 2
            pygame.draw.rect(glow_surf, (*NEON_YELLOW, alpha), 
                           (10-i, 10-i, title_text.get_width() + i*2, title_text.get_height() + i*2), 
                           border_radius=5)
        
        title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
        title_y = SCREEN_HEIGHT // 6 - title_text.get_height() // 2
        self.screen.blit(glow_surf, (title_x - 10, title_y - 10))
        self.screen.blit(title_text, (title_x, title_y))
        
        # Draw instructions with neon effect
        instructions = [
            "CATCH THE FRUITS WITH YOUR BASKET!",
            "AVOID BOMBS! BOMBS END THE GAME INSTANTLY!",
            "USE A AND D KEYS TO MOVE",
            "GAME ENDS WHEN YOU RUN OUT OF LIVES",
            "",
            "UNLIMITED MODE:",
            "- MANY FRUITS DROP AT ONCE",
            "- BOMBS DEDUCT 50 POINTS WHEN CAUGHT",
            "- 55 SECOND TIME LIMIT",
            "",
            "CLICK ANYWHERE TO RETURN"
        ]
        
        colors = [NEON_GREEN, NEON_RED, NEON_BLUE, NEON_YELLOW, WHITE, 
                 NEON_PURPLE, NEON_PURPLE, NEON_PURPLE, NEON_PURPLE, WHITE, NEON_PINK]
        
        for i, line in enumerate(instructions):
            color = colors[i % len(colors)]
            instr_text = self.font.render(line, True, color)
            
            # Add subtle glow for text
            if line:  # Skip empty lines
                glow_surf = pygame.Surface((instr_text.get_width() + 10, instr_text.get_height() + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*color, 30), 
                               (5, 5, instr_text.get_width(), instr_text.get_height()), 
                               border_radius=3)
                
                text_x = SCREEN_WIDTH // 2 - instr_text.get_width() // 2
                text_y = SCREEN_HEIGHT // 3 + i * 40
                self.screen.blit(glow_surf, (text_x - 5, text_y - 5))
            
            self.screen.blit(instr_text, 
                            (SCREEN_WIDTH // 2 - instr_text.get_width() // 2, 
                             SCREEN_HEIGHT // 3 + i * 40))
    
    def draw_game_screen(self):
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw basket with effects
        self.basket.draw_with_effects(self.screen)
        
        # Draw fruits with effects
        for sprite in self.fruits:
            sprite.draw_with_effects(self.screen)
        
        # Draw UI with neon effect
        self.draw_neon_text(f"SCORE: {self.score}", 20, 20, NEON_GREEN)
        
        # Draw different UI based on game mode
        if self.game_mode == "normal":
            self.draw_neon_text(f"LIVES: {self.lives}", 20, 60, NEON_RED)
            self.draw_neon_text(f"LEVEL: {self.level}", SCREEN_WIDTH - 150, 20, NEON_YELLOW)
            
            # Draw next milestone
            next_milestone = self.last_milestone + self.milestone_increment
            self.draw_neon_text(f"NEXT MILESTONE: {next_milestone}", SCREEN_WIDTH // 2, 60, NEON_YELLOW, center=True)
        else:
            # Draw timer for unlimited mode
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.timer_start_time
            remaining_time = max(0, self.unlimited_timer - elapsed_time)
            seconds_left = remaining_time // 1000
            
            # Make timer pulse red when low on time
            if seconds_left <= 10:
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 0.5 + 0.5
                timer_color = (NEON_RED[0], int(NEON_RED[1] * pulse), int(NEON_RED[2] * pulse))
            else:
                timer_color = NEON_YELLOW
            
            self.draw_neon_text(f"TIME: {seconds_left}s", SCREEN_WIDTH - 150, 20, timer_color)
            self.draw_neon_text("UNLIMITED MODE", SCREEN_WIDTH // 2, 60, NEON_PURPLE, center=True)
        
        # Draw speed boost indicator if active
        if self.speed_boosted:
            self.draw_neon_text("SPEED BOOST ACTIVE", SCREEN_WIDTH - 150, 100, NEON_RED)
        
        self.draw_neon_text("A: LEFT | D: RIGHT", SCREEN_WIDTH // 2, 20, NEON_CYAN, center=True)
        
        # Draw best score at the bottom left corner
        if self.best_score > 0:
            self.draw_neon_text(f"BEST: {self.best_score}", 20, SCREEN_HEIGHT - 40, NEON_YELLOW)
        
        # Draw mute button
        self.mute_button.draw(self.screen)
    
    def draw_neon_text(self, text, x, y, color, center=False):
        """Draw text with neon glow effect"""
        text_surface = self.font.render(text, True, color)
        
        # Create glow effect
        glow_surf = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 10), pygame.SRCALPHA)
        for i in range(5, 0, -1):
            alpha = 25 - i * 5
            pygame.draw.rect(glow_surf, (*color, alpha), 
                           (5-i, 5-i, text_surface.get_width() + i*2, text_surface.get_height() + i*2), 
                           border_radius=3)
        
        if center:
            x = x - text_surface.get_width() // 2
        
        self.screen.blit(glow_surf, (x - 5, y - 5))
        self.screen.blit(text_surface, (x, y))
    
    def draw_game_over_screen(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text with intense glow
        game_over_text = self.title_font.render("GAME OVER", True, NEON_RED)
        
        # Create pulsing glow effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.5 + 0.5
        glow_size = int(20 * pulse) + 10
        
        glow_surf = pygame.Surface((game_over_text.get_width() + glow_size*2, 
                                  game_over_text.get_height() + glow_size*2), pygame.SRCALPHA)
        
        for i in range(glow_size, 0, -2):
            alpha = min(150, int(20 - i * 0.5))
            pygame.draw.rect(glow_surf, (*NEON_RED, alpha), 
                           (glow_size-i, glow_size-i, 
                            game_over_text.get_width() + i*2, 
                            game_over_text.get_height() + i*2), 
                           border_radius=10)
        
        text_x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2
        text_y = SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50
        
        self.screen.blit(glow_surf, (text_x - glow_size, text_y - glow_size))
        self.screen.blit(game_over_text, (text_x, text_y))
        
        # Draw final score with glow
        final_score_text = self.font.render(f"FINAL SCORE: {self.score}", True, NEON_YELLOW)
        
        glow_surf = pygame.Surface((final_score_text.get_width() + 20, final_score_text.get_height() + 20), pygame.SRCALPHA)
        for i in range(10, 0, -2):
            alpha = 20 - i * 2
            pygame.draw.rect(glow_surf, (*NEON_YELLOW, alpha), 
                           (10-i, 10-i, final_score_text.get_width() + i*2, final_score_text.get_height() + i*2), 
                           border_radius=5)
        
        score_x = SCREEN_WIDTH // 2 - final_score_text.get_width() // 2
        score_y = SCREEN_HEIGHT // 2 + 20
        
        self.screen.blit(glow_surf, (score_x - 10, score_y - 10))
        self.screen.blit(final_score_text, (score_x, score_y))
    
    def draw(self):
        # Draw background
        self.background.draw(self.screen)
        
        # Draw current screen
        if self.current_screen == "home":
            self.draw_home_screen()
        elif self.current_screen == "game":
            self.draw_game_screen()
            
            # Draw game over screen if game is over
            if self.game_over:
                self.draw_game_over_screen()
        elif self.current_screen == "info":
            self.draw_info_screen()
        
        # Draw particles on top
        self.particles.draw(self.screen)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        # Game loop
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        # Clean up
        self.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
    def spawn_powerup(self):
        """Spawn a random power-up"""
        if self.game_mode != "unlimited":
            return  # Only spawn power-ups in unlimited mode
        
        # Choose a random power-up type
        power_type = random.choice(["time", "speed"])
        
        # Create the power-up at a random x position at the top of the screen
        x = random.randint(SCREEN_WIDTH // 6, 5 * SCREEN_WIDTH // 6)
        
        # Create and add the power-up
        from sprites import PowerUp
        new_powerup = PowerUp(x, 0, power_type, speed=3)
        self.all_sprites.add(new_powerup)
        self.powerups.add(new_powerup)
        
        # Play a sound effect
        self.sound_fx.play("correct")
    def spawn_powerup(self):
        """Spawn a random power-up"""
        if self.game_mode != "unlimited":
            return  # Only spawn power-ups in unlimited mode
        
        # Choose a random power-up type
        power_type = random.choice(["time", "speed"])
        
        # Create the power-up at a random x position at the top of the screen
        x = random.randint(SCREEN_WIDTH // 6, 5 * SCREEN_WIDTH // 6)
        
        # Create and add the power-up
        new_powerup = PowerUp(x, 0, power_type, speed=3)
        self.all_sprites.add(new_powerup)
        self.powerups.add(new_powerup)
        
        # Play a sound effect
        self.sound_fx.play("correct")
