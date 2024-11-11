import pygame
import math
import random

# Inicialización de Pygame
pygame.init()

# Constantes
WIDTH = 800
HEIGHT = 600
FPS = 60
GROUND_HEIGHT = 550

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Cohete Espacial")
clock = pygame.time.Clock()

class Rocket:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = GROUND_HEIGHT
        self.velocity = 0
        self.acceleration = 0
        self.mass = 1000  # kg
        self.fuel = 100  # porcentaje
        self.stage = 1
        self.particles = []
        self.smoke_particles = []
        self.flame_size = 0
        self.shake_offset = 0
        self.launch_started = False
        self.pre_launch_counter = 180  # 3 segundos a 60 FPS
        
    def start_launch_sequence(self):
        if not self.launch_started and self.pre_launch_counter > 0:
            self.pre_launch_counter -= 1
            if self.pre_launch_counter <= 0:
                self.launch_started = True
        
    def update(self):
        if not self.launch_started:
            self.start_launch_sequence()
            return
            
        # Física simplificada del cohete
        if self.fuel > 0:
            self.acceleration = 0.5  # Aceleración constante para simplificar
            self.fuel -= 0.1
            
            # Efecto de vibración
            self.shake_offset = random.randint(-2, 2) if self.y > GROUND_HEIGHT - 100 else 0
            
            # Generar partículas
            self.generate_particles()
            self.generate_smoke()
        else:
            self.acceleration = -0.1  # Gravedad simplificada
            
        self.velocity += self.acceleration
        self.y -= self.velocity
        
        # Actualizar partículas
        self.update_particles()
        self.update_smoke()
        
        # Actualizar tamaño de la llama
        self.flame_size = random.randint(30, 40) if self.fuel > 0 else 0
        
    def generate_particles(self):
        # Partículas para el efecto de propulsión
        for _ in range(3):
            particle = {
                'x': self.x + random.randint(-5, 5),
                'y': self.y + 30,
                'vel_x': random.uniform(-1, 1),
                'vel_y': random.uniform(2, 5),
                'size': random.randint(2, 4),
                'color': random.choice([YELLOW, ORANGE, RED]),
                'lifetime': 30
            }
            self.particles.append(particle)

    def generate_smoke(self):
        # Partículas de humo
        if self.y < GROUND_HEIGHT - 50:  # Solo generar humo después de cierta altura
            smoke = {
                'x': self.x + random.randint(-10, 10),
                'y': self.y + 40,
                'vel_x': random.uniform(-0.5, 0.5),
                'vel_y': random.uniform(0.5, 1.5),
                'size': random.randint(5, 15),
                'alpha': 255,
                'lifetime': 60
            }
            self.smoke_particles.append(smoke)
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)

    def update_smoke(self):
        for smoke in self.smoke_particles[:]:
            smoke['x'] += smoke['vel_x']
            smoke['y'] += smoke['vel_y']
            smoke['size'] += 0.2
            smoke['alpha'] = max(0, smoke['alpha'] - 4)
            smoke['lifetime'] -= 1
            if smoke['lifetime'] <= 0:
                self.smoke_particles.remove(smoke)
    
    def draw(self, surface):
        # Dibujar humo
        for smoke in self.smoke_particles:
            smoke_surface = pygame.Surface((smoke['size']*2, smoke['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surface, (200, 200, 200, smoke['alpha']), 
                             (smoke['size'], smoke['size']), smoke['size'])
            surface.blit(smoke_surface, (smoke['x'] - smoke['size'], smoke['y'] - smoke['size']))
        
        # Dibujar partículas de propulsión
        for particle in self.particles:
            pygame.draw.circle(surface, particle['color'],
                             (int(particle['x']), int(particle['y'])), particle['size'])
        
        # Dibujar llama del cohete
        if self.flame_size > 0:
            points = [
                (self.x - 8, self.y + 40),
                (self.x + 8, self.y + 40),
                (self.x, self.y + 40 + self.flame_size)
            ]
            pygame.draw.polygon(surface, ORANGE, points)
            points = [
                (self.x - 4, self.y + 40),
                (self.x + 4, self.y + 40),
                (self.x, self.y + 40 + self.flame_size - 10)
            ]
            pygame.draw.polygon(surface, YELLOW, points)
        
        # Dibujar cohete
        x_pos = self.x + self.shake_offset
        # Cuerpo principal
        pygame.draw.rect(surface, WHITE, 
                        (x_pos - 10, self.y - 40, 20, 40))
        # Punta
        pygame.draw.polygon(surface, RED,
                          [(x_pos - 10, self.y - 40),
                           (x_pos + 10, self.y - 40),
                           (x_pos, self.y - 50)])
        # Aletas
        pygame.draw.polygon(surface, GRAY,
                          [(x_pos - 10, self.y),
                           (x_pos - 20, self.y + 10),
                           (x_pos - 10, self.y - 10)])
        pygame.draw.polygon(surface, GRAY,
                          [(x_pos + 10, self.y),
                           (x_pos + 20, self.y + 10),
                           (x_pos + 10, self.y - 10)])

class Simulation:
    def __init__(self):
        self.rocket = Rocket()
        self.running = True
        self.background = BLACK
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), 
                      random.random()) for _ in range(200)]
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        self.rocket.update()
        
    def draw(self):
        screen.fill(self.background)
        
        # Dibujar estrellas con parpadeo
        for i, (x, y, brightness) in enumerate(self.stars):
            # Hacer que las estrellas parpadeen
            current_brightness = brightness * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.001 + i))
            color = (int(255 * current_brightness),) * 3
            pygame.draw.circle(screen, color, (int(x), int(y)), 1)
        
        # Dibujar suelo con degradado
        for i in range(50):
            color = max(0, min(255, 128 - i*2))
            pygame.draw.rect(screen, (color, color, color),
                           (0, GROUND_HEIGHT + i, WIDTH, 1))
        
        # Dibujar cohete
        self.rocket.draw(screen)
        
        # Dibujar información
        font = pygame.font.Font(None, 36)
        
        if not self.rocket.launch_started:
            countdown = f"T-{self.rocket.pre_launch_counter//60 + 1}"
            countdown_text = font.render(countdown, True, RED)
            text_rect = countdown_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(countdown_text, text_rect)
        
        fuel_text = font.render(f"Combustible: {int(self.rocket.fuel)}%", True, WHITE)
        height_text = font.render(f"Altura: {int(GROUND_HEIGHT - self.rocket.y)}m", True, WHITE)
        velocity_text = font.render(f"Velocidad: {int(self.rocket.velocity*10)}m/s", True, WHITE)
        
        screen.blit(fuel_text, (10, 10))
        screen.blit(height_text, (10, 50))
        screen.blit(velocity_text, (10, 90))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    pygame.quit()