import pygame
import os
import random
import math

# Enhanced color palette (neon retro style)
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

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, fruit_type, side, speed):
        super().__init__()
        self.fruit_type = fruit_type
        self.side = side
        self.speed = speed
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        self.pulse_factor = 0
        self.pulse_speed = random.uniform(0.05, 0.1)
        
        # Create enhanced pixel art for the fruit
        self.original_image = self.create_enhanced_fruit(fruit_type)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Add glow effect
        self.glow_color = self.get_glow_color(fruit_type)
        self.glow_radius = self.rect.width // 2 + 4
    
    def get_glow_color(self, fruit_type):
        if fruit_type == "apple":
            return NEON_RED
        elif fruit_type == "banana":
            return NEON_YELLOW
        elif fruit_type == "orange":
            return NEON_ORANGE
        elif fruit_type == "bomb":
            return (100, 100, 100)
        # Removed rotten fruit case
        elif fruit_type == "star_fruit":
            return NEON_YELLOW
        elif fruit_type == "blueberry":
            return NEON_BLUE
        else:
            return NEON_PURPLE
    
    def create_enhanced_fruit(self, fruit_type):
        # Create a surface for the fruit with higher resolution
        size = 48
        image = pygame.Surface((size, size))
        image.fill((0, 0, 0))
        image.set_colorkey((0, 0, 0))  # Make black transparent
        
        # Draw different fruits based on type with enhanced details
        if fruit_type == "apple":
            color = NEON_RED
            # Draw apple body
            pygame.draw.circle(image, color, (size//2, size//2 + 2), size//2 - 6)
            # Add highlight
            highlight = pygame.Surface((size//4, size//4), pygame.SRCALPHA)
            pygame.draw.circle(highlight, (255, 255, 255, 100), (size//8, size//8), size//8)
            image.blit(highlight, (size//3, size//3))
            # Draw stem
            pygame.draw.rect(image, (139, 90, 40), (size//2 - 2, 6, 4, 8))
            # Add leaf
            leaf_points = [(size//2, 8), (size//2 + 8, 4), (size//2 + 4, 12)]
            pygame.draw.polygon(image, NEON_GREEN, leaf_points)
        
        elif fruit_type == "banana":
            color = NEON_YELLOW
            # Draw banana shape (curved rectangle with more detail)
            points = [(size//4, size//3), (3*size//4, size//4), 
                     (7*size//8, size//2), (3*size//4, 3*size//4),
                     (size//4, 2*size//3), (size//8, size//2)]
            pygame.draw.polygon(image, color, points)
            # Add highlights
            pygame.draw.line(image, WHITE, (size//3, size//2), (2*size//3, size//2 - 4), 2)
            # Add details
            pygame.draw.line(image, (color[0]//2, color[1]//2, color[2]//2), 
                            (size//4 + 4, size//2), (3*size//4 - 4, size//2), 3)
        
        elif fruit_type == "orange":
            color = NEON_ORANGE
            # Draw orange body
            pygame.draw.circle(image, color, (size//2, size//2), size//2 - 6)
            # Add highlight
            highlight = pygame.Surface((size//3, size//3), pygame.SRCALPHA)
            pygame.draw.circle(highlight, (255, 255, 255, 80), (size//6, size//6), size//6)
            image.blit(highlight, (size//3, size//3))
            # Add texture details (segments)
            for i in range(6):
                angle = i * math.pi / 3
                x1 = size//2
                y1 = size//2
                x2 = int(x1 + (size//2 - 8) * math.cos(angle))
                y2 = int(y1 + (size//2 - 8) * math.sin(angle))
                pygame.draw.line(image, (color[0]//1.2, color[1]//1.2, color[2]//1.2), (x1, y1), (x2, y2), 2)
        
        elif fruit_type == "bomb":
            # Draw bomb body
            pygame.draw.circle(image, (30, 30, 30), (size//2, size//2 + 2), size//2 - 6)
            # Add highlight
            highlight = pygame.Surface((size//4, size//4), pygame.SRCALPHA)
            pygame.draw.circle(highlight, (100, 100, 100, 100), (size//8, size//8), size//8)
            image.blit(highlight, (size//3, size//3))
            # Draw fuse
            pygame.draw.rect(image, (139, 90, 40), (size//2 - 1, 6, 3, 8))
            # Draw flame
            flame_points = [(size//2, 2), (size//2 - 4, 8), (size//2, 5), (size//2 + 4, 8)]
            pygame.draw.polygon(image, NEON_RED, flame_points)
            pygame.draw.polygon(image, NEON_YELLOW, [(size//2, 3), (size//2 - 2, 7), (size//2, 5), (size//2 + 2, 7)])
        
        # Removed rotten fruit type
        
        elif fruit_type == "star_fruit":
            # New fruit: star fruit
            color = NEON_YELLOW
            # Draw star shape
            points = []
            for i in range(5):
                angle = math.pi/2 + i * 2*math.pi/5
                # Outer point
                x = size//2 + int((size//2 - 6) * math.cos(angle))
                y = size//2 + int((size//2 - 6) * math.sin(angle))
                points.append((x, y))
                # Inner point
                angle += math.pi/5
                x = size//2 + int((size//4) * math.cos(angle))
                y = size//2 + int((size//4) * math.sin(angle))
                points.append((x, y))
            pygame.draw.polygon(image, color, points)
            # Add highlight
            highlight = pygame.Surface((size//4, size//4), pygame.SRCALPHA)
            pygame.draw.circle(highlight, (255, 255, 255, 100), (size//8, size//8), size//8)
            image.blit(highlight, (size//3, size//3))
        
        elif fruit_type == "blueberry":
            # New fruit: blueberry
            color = NEON_BLUE
            # Draw blueberry body
            pygame.draw.circle(image, color, (size//2, size//2), size//2 - 6)
            # Add highlight
            highlight = pygame.Surface((size//4, size//4), pygame.SRCALPHA)
            pygame.draw.circle(highlight, (255, 255, 255, 100), (size//8, size//8), size//8)
            image.blit(highlight, (size//3, size//3))
            # Add stem
            pygame.draw.rect(image, (100, 70, 40), (size//2 - 1, 8, 2, 4))
            # Add texture dots
            for _ in range(10):
                angle = random.uniform(0, 2*math.pi)
                dist = random.randint(size//6, size//2 - 8)
                x = int(size//2 + dist * math.cos(angle))
                y = int(size//2 + dist * math.sin(angle))
                pygame.draw.circle(image, (color[0]//1.5, color[1]//1.5, color[2]//1.5), (x, y), 2)
        
        return image
    
    def update(self):
        # Move the fruit down
        self.rect.y += self.speed
        
        # Add a slight wobble
        self.rect.x += random.randint(-1, 1)
        
        # Rotate the fruit
        self.rotation += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        
        # Update rect to maintain center position
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Pulse effect
        self.pulse_factor += self.pulse_speed
        if self.pulse_factor > 1:
            self.pulse_factor = 0
    
    def draw(self, surface):
        """Draw the fruit directly to a surface with glow effect"""
        # Draw glow effect
        if self.fruit_type not in ["bomb", "rotten"]:
            glow_surf = pygame.Surface((self.glow_radius*2, self.glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.glow_color, 100), (self.glow_radius, self.glow_radius), self.glow_radius)
            surface.blit(glow_surf, (self.rect.centerx - self.glow_radius, self.rect.centery - self.glow_radius), special_flags=pygame.BLEND_ADD)
        
        # Draw the fruit
        surface.blit(self.image, self.rect)
    
    def draw_with_effects(self, surface):
        """Draw the fruit with all visual effects"""
        # Draw glow effect
        if self.fruit_type not in ["bomb", "rotten"]:
            pulse = abs(math.sin(self.pulse_factor * 2 * math.pi)) * 0.3 + 0.7
            glow_radius = int(self.glow_radius * pulse)
            glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.glow_color, 100), (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surf, (self.rect.centerx - glow_radius, self.rect.centery - glow_radius), special_flags=pygame.BLEND_ADD)
        
        # Draw the fruit
        surface.blit(self.image, self.rect)

class Basket(pygame.sprite.Sprite):
    def __init__(self, x, y, side):
        super().__init__()
        self.side = side
        
        # Create enhanced pixel art for the basket
        self.original_image = self.create_enhanced_basket()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Movement
        self.speed = 10
        self.target_x = x
        self.smooth_factor = 0.2
        
        # Visual effects
        self.glow_color = NEON_PURPLE
        self.glow_radius = self.rect.width // 2 + 10
        self.pulse_factor = 0
        self.pulse_speed = 0.03
    
    def create_enhanced_basket(self):
        # Create a surface for the basket with higher resolution
        width, height = 100, 50
        image = pygame.Surface((width, height))
        image.fill((0, 0, 0))
        image.set_colorkey((0, 0, 0))  # Make black transparent
        
        # Choose color for basket
        color = NEON_PURPLE
        
        # Draw basket body with more detail
        pygame.draw.rect(image, color, (0, height//2, width, height//2))
        pygame.draw.rect(image, color, (0, 0, 6, height//2))
        pygame.draw.rect(image, color, (width-6, 0, 6, height//2))
        
        # Add basket weave pattern
        for i in range(0, width, 10):
            pygame.draw.line(image, (color[0]//2, color[1]//2, color[2]//2), 
                            (i, height//2), (i, height), 2)
        
        for i in range(0, height//2, 6):
            pygame.draw.line(image, (color[0]//2, color[1]//2, color[2]//2), 
                            (0, height//2 + i), (width, height//2 + i), 1)
        
        # Add highlights
        pygame.draw.line(image, (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)), 
                        (2, height//2), (width-2, height//2), 2)
        
        return image
    
    def move_left(self):
        self.target_x -= self.speed
    
    def move_right(self):
        self.target_x += self.speed
    
    def update(self):
        # Smooth movement towards target
        self.rect.x += (self.target_x - self.rect.centerx) * self.smooth_factor
        
        # Keep basket within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.target_x = self.rect.centerx
        if self.rect.right > 800:  # Screen width
            self.rect.right = 800
            self.target_x = self.rect.centerx
        
        # Update pulse effect
        self.pulse_factor += self.pulse_speed
        if self.pulse_factor > 1:
            self.pulse_factor = 0
    
    def draw_with_effects(self, surface):
        """Draw the basket with glow effect"""
        # Draw glow effect
        pulse = abs(math.sin(self.pulse_factor * 2 * math.pi)) * 0.3 + 0.7
        glow_radius = int(self.glow_radius * pulse)
        glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.glow_color, 80), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surf, (self.rect.centerx - glow_radius, self.rect.centery - glow_radius), special_flags=pygame.BLEND_ADD)
        
        # Draw the basket
        surface.blit(self.image, self.rect)

class Conveyor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Create enhanced pixel art for the conveyor
        self.image = self.create_enhanced_conveyor()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Animation
        self.frame = 0
        self.animation_speed = 1
    
    def create_enhanced_conveyor(self):
        # Create a surface for the conveyor with higher resolution
        width, height = 500, 30
        image = pygame.Surface((width, height))
        image.fill((0, 0, 0))
        image.set_colorkey((0, 0, 0))  # Make black transparent
        
        # Draw conveyor body with metallic look
        pygame.draw.rect(image, (120, 120, 140), (0, 0, width, height))
        
        # Add conveyor belt pattern
        for i in range(0, width, 20):
            pygame.draw.rect(image, (70, 70, 90), (i, 0, 10, height))
        
        # Add highlights
        for i in range(0, width, 40):
            pygame.draw.line(image, (150, 150, 170), (i, 2), (i + 20, 2), 2)
        
        # Add side details
        pygame.draw.rect(image, (100, 100, 120), (0, 0, width, 4))
        pygame.draw.rect(image, (100, 100, 120), (0, height-4, width, 4))
        
        return image
    
    def update(self):
        # Animate the conveyor
        self.frame = (self.frame + self.animation_speed) % 20
        
        # Create a new image with updated pattern
        width, height = 500, 30
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        # Draw conveyor body
        pygame.draw.rect(self.image, (120, 120, 140), (0, 0, width, height))
        
        # Add animated conveyor belt pattern
        offset = self.frame
        for i in range(-offset, width, 20):
            pygame.draw.rect(self.image, (70, 70, 90), (i, 0, 10, height))
        
        # Add highlights
        for i in range(-offset % 40, width, 40):
            pygame.draw.line(self.image, (150, 150, 170), (i, 2), (i + 20, 2), 2)
        
        # Add side details
        pygame.draw.rect(self.image, (100, 100, 120), (0, 0, width, 4))
        pygame.draw.rect(self.image, (100, 100, 120), (0, height-4, width, 4))

class Button:
    def __init__(self, x, y, width, height, text, color, is_icon=False):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.current_color = self.color
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False
        self.is_icon = is_icon
        
        # Create pixel art border
        self.border_width = 4
        
        # Visual effects
        self.glow_color = color
        self.glow_radius = max(width, height) // 2 + 10
        self.pulse_factor = 0
        self.pulse_speed = 0.03
    
    def update(self, mouse_pos):
        # Check if mouse is hovering over button
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        
        # Update pulse effect
        self.pulse_factor += self.pulse_speed
        if self.pulse_factor > 1:
            self.pulse_factor = 0
    
    def is_clicked(self, click_pos):
        return self.rect.collidepoint(click_pos)
    
    def draw(self, surface):
        # Draw glow effect if hovered
        if self.is_hovered:
            pulse = abs(math.sin(self.pulse_factor * 2 * math.pi)) * 0.3 + 0.7
            glow_radius = int(self.glow_radius * pulse)
            glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.glow_color, 100), (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surf, (self.rect.centerx - glow_radius, self.rect.centery - glow_radius), special_flags=pygame.BLEND_ADD)
        
        # Draw button with pixel art style
        pygame.draw.rect(surface, self.current_color, self.rect)
        
        # Draw pixel art border
        border_rects = [
            # Top border
            pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.border_width),
            # Bottom border
            pygame.Rect(self.rect.left, self.rect.bottom - self.border_width, self.rect.width, self.border_width),
            # Left border
            pygame.Rect(self.rect.left, self.rect.top, self.border_width, self.rect.height),
            # Right border
            pygame.Rect(self.rect.right - self.border_width, self.rect.top, self.border_width, self.rect.height)
        ]
        
        # Draw borders with darker color
        border_color = (self.current_color[0] // 2, self.current_color[1] // 2, self.current_color[2] // 2)
        for border_rect in border_rects:
            pygame.draw.rect(surface, border_color, border_rect)
        
        if self.is_icon and self.text in ["speaker", "speaker-muted"]:
            self.draw_speaker_icon(surface, self.text == "speaker-muted")
        else:
            # Draw text with shadow
            text_surface = self.font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
            surface.blit(text_surface, text_rect)
            
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
    
    def draw_speaker_icon(self, surface, muted=False):
        # Draw speaker icon
        icon_color = WHITE
        
        # Speaker body
        speaker_rect = pygame.Rect(self.rect.centerx - 8, self.rect.centery - 6, 6, 12)
        pygame.draw.rect(surface, icon_color, speaker_rect)
        
        # Speaker cone
        points = [
            (self.rect.centerx - 2, self.rect.centery - 6),
            (self.rect.centerx + 6, self.rect.centery - 10),
            (self.rect.centerx + 6, self.rect.centery + 10),
            (self.rect.centerx - 2, self.rect.centery + 6)
        ]
        pygame.draw.polygon(surface, icon_color, points)
        
        if not muted:
            # Sound waves
            for i in range(1, 3):
                radius = 4 + i * 3
                pygame.draw.arc(surface, icon_color,
                              (self.rect.centerx + 6, self.rect.centery - radius, radius * 2, radius * 2),
                              -math.pi/3, math.pi/3, 2)
        else:
            # X mark for muted
            pygame.draw.line(surface, NEON_RED, 
                           (self.rect.centerx + 4, self.rect.centery - 8),
                           (self.rect.centerx + 12, self.rect.centery + 8), 2)
            pygame.draw.line(surface, NEON_RED, 
                           (self.rect.centerx + 12, self.rect.centery - 8),
                           (self.rect.centerx + 4, self.rect.centery + 8), 2)

class Particle:
    def __init__(self, x, y, color, size=3, speed=2):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = random.randint(20, 60)
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
    
    def draw(self, surface):
        alpha = min(255, int(255 * self.lifetime / 30))
        particle_color = (*self.color, alpha)
        particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, particle_color, (self.size, self.size), self.size)
        surface.blit(particle_surf, (int(self.x - self.size), int(self.y - self.size)), special_flags=pygame.BLEND_ADD)

class CrackleParticle(Particle):
    def __init__(self, x, y, color, size=2, speed=3, angle_offset=0):
        super().__init__(x, y, color, size, speed)
        self.angle_offset = angle_offset
        self.zigzag_counter = 0
        self.zigzag_freq = random.uniform(0.2, 0.4)
        self.lifetime = random.randint(10, 30)  # Shorter lifetime for crackle
        
    def update(self):
        # Create zigzag motion by changing angle periodically
        self.zigzag_counter += self.zigzag_freq
        if self.zigzag_counter >= 1.0:
            self.angle += self.angle_offset * random.uniform(0.5, 1.5) * math.pi
            self.zigzag_counter = 0
            
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        
        # Particles get smaller as they age
        self.size = max(0, self.size - 0.05)
    
    def draw(self, surface):
        # Brighter glow for electric effect
        alpha = min(255, int(255 * self.lifetime / 20))
        particle_color = (*self.color, alpha)
        
        # Draw a line instead of a circle for electric look
        if self.lifetime > 5:  # Only draw if particle is still visible
            end_x = int(self.x + math.cos(self.angle) * self.size * 2)
            end_y = int(self.y + math.sin(self.angle) * self.size * 2)
            
            # Draw glow
            glow_surf = pygame.Surface((int(self.size * 6), int(self.size * 6)), pygame.SRCALPHA)
            pygame.draw.line(glow_surf, 
                           (particle_color[0], particle_color[1], particle_color[2], alpha//3),
                           (int(self.size * 3 - (end_x - self.x)/2), int(self.size * 3 - (end_y - self.y)/2)),
                           (int(self.size * 3 + (end_x - self.x)/2), int(self.size * 3 + (end_y - self.y)/2)),
                           int(self.size * 2))
            
            surface.blit(glow_surf, 
                       (int(self.x - self.size * 3), int(self.y - self.size * 3)), 
                       special_flags=pygame.BLEND_ADD)
            
            # Draw core
            pygame.draw.line(surface, 
                           (255, 255, 255, alpha),
                           (int(self.x), int(self.y)),
                           (end_x, end_y),
                           max(1, int(self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particles(self, x, y, color, count=10):
        for _ in range(count):
            size = random.uniform(2, 5)
            speed = random.uniform(1, 3)
            self.particles.append(Particle(x, y, color, size, speed))
    
    def add_crackle(self, x, y, color=NEON_CYAN):
        """Add a crackle effect (electric-like particles)"""
        for _ in range(20):
            size = random.uniform(1, 3)
            speed = random.uniform(2, 5)
            angle_offset = random.uniform(-0.5, 0.5)  # For zigzag effect
            self.particles.append(CrackleParticle(x, y, color, size, speed, angle_offset))
    
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []
        self.generate_stars(150)
        self.scroll_speed = 0.5
        self.offset = 0
        
        # Star Wars elements
        # Tatooine-like planet
        self.planet_pos = (width * 0.8, height * 0.2)
        self.planet_radius = 80
        self.planet_color = (230, 190, 110)  # Sandy color for Tatooine
        
        # Ships
        self.tie_fighters = []
        self.x_wings = []
        self.generate_tie_fighters(4)
        self.generate_x_wings(3)
        
        # Laser shots
        self.lasers = []
        self.laser_timer = 0
        self.explosion_particles = []
    
    def generate_stars(self, count):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 3)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            self.stars.append((x, y, size, color))
    
    def generate_tie_fighters(self, count):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height // 3)
            size = random.randint(15, 25)
            speed = random.uniform(0.5, 1.2)
            self.tie_fighters.append([x, y, size, speed])
    
    def generate_x_wings(self, count):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(self.height // 4, self.height // 2)
            size = random.randint(15, 25)
            speed = random.uniform(0.7, 1.5)
            self.x_wings.append([x, y, size, speed])
    
    def update(self):
        self.offset = (self.offset + self.scroll_speed) % self.height
        
        # Update TIE fighters
        for fighter in self.tie_fighters:
            fighter[0] += fighter[3]  # Move horizontally
            if fighter[0] > self.width + fighter[2]:
                fighter[0] = -fighter[2]
                fighter[1] = random.randint(0, self.height // 3)
        
        # Update X-Wings
        for x_wing in self.x_wings:
            x_wing[0] -= x_wing[3]  # Move in opposite direction
            if x_wing[0] < -x_wing[2]:
                x_wing[0] = self.width + x_wing[2]
                x_wing[1] = random.randint(self.height // 4, self.height // 2)
        
        # Update laser shots
        self.laser_timer += 1
        if self.laser_timer >= 20:  # Fire lasers more frequently
            self.laser_timer = 0
            
            # Random chance for each ship to fire
            for x_wing in self.x_wings:
                if random.random() < 0.3:  # 30% chance to fire
                    # Find closest TIE fighter
                    closest_tie = None
                    min_dist = float('inf')
                    for tie in self.tie_fighters:
                        dist = ((x_wing[0] - tie[0])**2 + (x_wing[1] - tie[1])**2)**0.5
                        if dist < min_dist:
                            min_dist = dist
                            closest_tie = tie
                    
                    if closest_tie:
                        # X-Wing fires red laser
                        self.lasers.append([x_wing[0], x_wing[1], closest_tie[0], closest_tie[1], (255, 0, 0), 20])
            
            for tie in self.tie_fighters:
                if random.random() < 0.3:  # 30% chance to fire
                    # Find closest X-Wing
                    closest_x_wing = None
                    min_dist = float('inf')
                    for x_wing in self.x_wings:
                        dist = ((tie[0] - x_wing[0])**2 + (tie[1] - x_wing[1])**2)**0.5
                        if dist < min_dist:
                            min_dist = dist
                            closest_x_wing = x_wing
                    
                    if closest_x_wing:
                        # TIE fighter fires green laser
                        self.lasers.append([tie[0], tie[1], closest_x_wing[0], closest_x_wing[1], (0, 255, 0), 20])
        
        # Update existing lasers
        for laser in self.lasers[:]:
            # Calculate direction vector
            dx = laser[2] - laser[0]
            dy = laser[3] - laser[1]
            length = max(0.1, math.sqrt(dx*dx + dy*dy))
            dx, dy = dx/length, dy/length
            
            # Move laser
            speed = 8
            laser[0] += dx * speed
            laser[1] += dy * speed
            
            # Decrease lifetime
            laser[5] -= 1
            
            # Check if laser has reached target or expired
            if laser[5] <= 0 or (abs(laser[0] - laser[2]) < 10 and abs(laser[1] - laser[3]) < 10):
                # Create explosion at target
                self.create_explosion(laser[2], laser[3], laser[4])
                self.lasers.remove(laser)
        
        # Update explosion particles
        for particle in self.explosion_particles[:]:
            particle[0] += particle[3]  # x position
            particle[1] += particle[4]  # y position
            particle[5] -= 1  # lifetime
            
            if particle[5] <= 0:
                self.explosion_particles.remove(particle)
    
    def create_explosion(self, x, y, color):
        # Create particles for explosion
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 3)
            size = random.uniform(1, 4)
            lifetime = random.randint(10, 30)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.explosion_particles.append([x, y, size, dx, dy, lifetime, color])
    
    def draw(self, surface):
        # Draw plain black background
        surface.fill((0, 0, 0))  # Pure black background
        
        # Draw laser shots
        for laser in self.lasers:
            start_x, start_y, end_x, end_y, color, _ = laser
            pygame.draw.line(surface, color, (int(start_x), int(start_y)), 
                           (int(start_x + (end_x - start_x) * 0.2), 
                            int(start_y + (end_y - start_y) * 0.2)), 3)
            
            # Draw glow effect
            glow_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, 150), (4, 4), 4)
            surface.blit(glow_surf, (int(start_x) - 4, int(start_y) - 4), special_flags=pygame.BLEND_ADD)
        
        # Draw explosion particles
        for particle in self.explosion_particles:
            x, y, size, _, _, _, color = particle
            pygame.draw.circle(surface, color, (int(x), int(y)), int(size))
            
            # Draw glow
            glow_surf = pygame.Surface((int(size*4), int(size*4)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, 50), (int(size*2), int(size*2)), int(size*2))
            surface.blit(glow_surf, (int(x - size*2), int(y - size*2)), special_flags=pygame.BLEND_ADD)
        
        # Draw Tatooine-like planet
        x, y = self.planet_pos
        radius = self.planet_radius
        
        # Main planet body
        pygame.draw.circle(surface, self.planet_color, (int(x), int(y)), radius)
        
        # Add some craters/details
        for _ in range(5):
            crater_x = x + random.randint(-radius//2, radius//2)
            crater_y = y + random.randint(-radius//2, radius//2)
            crater_radius = random.randint(5, 15)
            
            # Only draw if within planet bounds
            if ((crater_x - x)**2 + (crater_y - y)**2)**0.5 < radius - crater_radius:
                # Slightly darker color for craters
                crater_color = (self.planet_color[0] - 30, self.planet_color[1] - 30, self.planet_color[2] - 30)
                pygame.draw.circle(surface, crater_color, (int(crater_x), int(crater_y)), crater_radius)
        
        # Add highlight
        highlight_pos = (int(x - radius * 0.3), int(y - radius * 0.3))
        highlight_radius = int(radius * 0.4)
        highlight_color = (min(self.planet_color[0] + 20, 255), 
                          min(self.planet_color[1] + 20, 255), 
                          min(self.planet_color[2] + 20, 255))
        pygame.draw.circle(surface, highlight_color, highlight_pos, highlight_radius)
        
        # Draw TIE fighters
        for x, y, size, speed in self.tie_fighters:
            # Wing panels
            wing_color = (70, 70, 70)
            pygame.draw.rect(surface, wing_color, 
                           (int(x - size), int(y - size//2), 
                            size//2, size))
            pygame.draw.rect(surface, wing_color, 
                           (int(x + size//2), int(y - size//2), 
                            size//2, size))
            
            # Center pod
            pygame.draw.circle(surface, (100, 100, 100), 
                             (int(x), int(y)), size//3)
        
        # Draw X-Wings
        for x, y, size, speed in self.x_wings:
            x_wing_color = (150, 150, 150)
            
            # Main body
            pygame.draw.rect(surface, x_wing_color, 
                           (int(x - 20), int(y - 5), 40, 10))
            
            # Wings
            pygame.draw.polygon(surface, x_wing_color, 
                              [(int(x - 15), int(y)), 
                               (int(x - 30), int(y - 15)), 
                               (int(x - 10), int(y - 5))])
            pygame.draw.polygon(surface, x_wing_color, 
                              [(int(x - 15), int(y)), 
                               (int(x - 30), int(y + 15)), 
                               (int(x - 10), int(y + 5))])
            pygame.draw.polygon(surface, x_wing_color, 
                              [(int(x + 15), int(y)), 
                               (int(x + 30), int(y - 15)), 
                               (int(x + 10), int(y - 5))])
            pygame.draw.polygon(surface, x_wing_color, 
                              [(int(x + 15), int(y)), 
                               (int(x + 30), int(y + 15)), 
                               (int(x + 10), int(y + 5))])
            
            # Engine glow
            pygame.draw.circle(surface, (255, 100, 50), 
                             (int(x - 20), int(y)), 3)
