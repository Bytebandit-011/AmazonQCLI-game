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
        # Create particles for explosion (visual only, no sound)
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
