import pygame
import math
import random

# Inicialización de Pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 600
FPS = 60
ALTURA_SUELO = 550

# Constantes físicas
GRAVEDAD = 9.81
G = 6.673E-11
MASA_TIERRA = 5.972E24

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 0, 255)
GRIS = (128, 128, 128)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Cohete Espacial")
reloj = pygame.time.Clock()

class Cohete:
    def __init__(self, masa_propelente, masa_estructural, masa_satelite, impulso_especifico):
        # Variables de la física del cohete
        self.masa_propelente = masa_propelente
        self.masa_estructural = masa_estructural
        self.masa_satelite = masa_satelite
        self.impulso_especifico = impulso_especifico
        
        # Variables de visualización
        self.x = ANCHO // 2
        self.y = ALTURA_SUELO
        self.velocidad = 0
        self.aceleracion = 0
        self.particulas = []
        self.particulas_humo = []
        self.tamano_llama = 0
        self.desplazamiento_vibracion = 0
        self.lanzamiento_iniciado = False
        self.contador_prelanzamiento = 180
        
        # Inicializar cálculos físicos
        self.calcular_masas_totales()
        self.calcular_relacion_masas()
        self.calcular_velocidad_inicial()
        self.calcular_flujo_masico()
        
    def calcular_masas_totales(self):
        self.masa_etapa3 = self.masa_propelente[2] + self.masa_estructural[2] + self.masa_satelite
        self.masa_etapa2 = self.masa_propelente[1] + self.masa_estructural[1] + self.masa_etapa3
        self.masa_etapa1 = self.masa_propelente[0] + self.masa_estructural[0] + self.masa_etapa2
        return self.masa_etapa1, self.masa_etapa2, self.masa_etapa3
    
    def calcular_relacion_masas(self):
        self.relacion1 = self.masa_etapa1 / (self.masa_estructural[0] + self.masa_satelite)
        self.relacion2 = self.masa_etapa2 / (self.masa_estructural[1] + self.masa_satelite)
        self.relacion3 = self.masa_etapa3 / (self.masa_estructural[2] + self.masa_satelite)
        return self.relacion1, self.relacion2, self.relacion3
    
    def calcular_velocidad_inicial(self):
        self.vel_etapa1 = self.impulso_especifico[0] * GRAVEDAD
        self.vel_etapa2 = self.impulso_especifico[1] * GRAVEDAD
        self.vel_etapa3 = self.impulso_especifico[2] * GRAVEDAD
        return [self.vel_etapa1, self.vel_etapa2, self.vel_etapa3]
    
    def calcular_flujo_masico(self):
        self.flujo_masico1 = self.masa_propelente[0] / self.impulso_especifico[0]
        self.flujo_masico2 = self.masa_propelente[1] / self.impulso_especifico[1]
        self.flujo_masico3 = self.masa_propelente[2] / self.impulso_especifico[2]
        return self.flujo_masico1, self.flujo_masico2, self.flujo_masico3
    
    def calcular_fuerzas(self):
        self.fuerza1 = self.vel_etapa1 * self.flujo_masico1
        self.fuerza2 = self.vel_etapa2 * self.flujo_masico2
        self.fuerza3 = self.vel_etapa3 * self.flujo_masico3
        return self.fuerza1, self.fuerza2, self.fuerza3
    
    def iniciar_secuencia_lanzamiento(self):
        if not self.lanzamiento_iniciado and self.contador_prelanzamiento > 0:
            self.contador_prelanzamiento -= 1
            if self.contador_prelanzamiento <= 0:
                self.lanzamiento_iniciado = True
    
    def actualizar(self):
        if not self.lanzamiento_iniciado:
            self.iniciar_secuencia_lanzamiento()
            return
            
        # Cálculos físicos basados en las etapas
        if self.masa_propelente[0] > 0:  # Primera etapa
            self.calcular_fuerzas()
            self.aceleracion = self.fuerza1 / self.masa_etapa1 - GRAVEDAD
            self.masa_propelente[0] -= self.flujo_masico1 / FPS
            
            # Efecto de vibración
            self.desplazamiento_vibracion = random.randint(-2, 2) if self.y > ALTURA_SUELO - 100 else 0
            
            # Generar efectos visuales
            self.generar_particulas()
            self.generar_humo()
        else:
            self.aceleracion = -GRAVEDAD
            
        self.velocidad += self.aceleracion
        self.y -= self.velocidad
        
        # Actualizar efectos visuales
        self.actualizar_particulas()
        self.actualizar_humo()
        
        # Actualizar tamaño de la llama
        self.tamano_llama = random.randint(30, 40) if self.masa_propelente[0] > 0 else 0
        
    def generar_particulas(self):
        for _ in range(3):
            particula = {
                'x': self.x + random.randint(-5, 5),
                'y': self.y + 30,
                'vel_x': random.uniform(-1, 1),
                'vel_y': random.uniform(2, 5),
                'tamano': random.randint(2, 4),
                'color': random.choice([AMARILLO, NARANJA, ROJO]),
                'vida': 30
            }
            self.particulas.append(particula)

    def generar_humo(self):
        if self.y < ALTURA_SUELO - 50:
            humo = {
                'x': self.x + random.randint(-10, 10),
                'y': self.y + 40,
                'vel_x': random.uniform(-0.5, 0.5),
                'vel_y': random.uniform(0.5, 1.5),
                'tamano': random.randint(5, 15),
                'alpha': 255,
                'vida': 60
            }
            self.particulas_humo.append(humo)
    
    def actualizar_particulas(self):
        for particula in self.particulas[:]:
            particula['x'] += particula['vel_x']
            particula['y'] += particula['vel_y']
            particula['vida'] -= 1
            if particula['vida'] <= 0:
                self.particulas.remove(particula)

    def actualizar_humo(self):
        for humo in self.particulas_humo[:]:
            humo['x'] += humo['vel_x']
            humo['y'] += humo['vel_y']
            humo['tamano'] += 0.2
            humo['alpha'] = max(0, humo['alpha'] - 4)
            humo['vida'] -= 1
            if humo['vida'] <= 0:
                self.particulas_humo.remove(humo)
    
    def dibujar(self, superficie):
        # Dibujar humo
        for humo in self.particulas_humo:
            superficie_humo = pygame.Surface((humo['tamano']*2, humo['tamano']*2), pygame.SRCALPHA)
            pygame.draw.circle(superficie_humo, (200, 200, 200, humo['alpha']), 
                             (humo['tamano'], humo['tamano']), humo['tamano'])
            superficie.blit(superficie_humo, (humo['x'] - humo['tamano'], humo['y'] - humo['tamano']))
        
        # Dibujar partículas de propulsión
        for particula in self.particulas:
            pygame.draw.circle(superficie, particula['color'],
                             (int(particula['x']), int(particula['y'])), particula['tamano'])
        
        # Dibujar llama del cohete
        if self.tamano_llama > 0:
            puntos = [
                (self.x - 8, self.y + 40),
                (self.x + 8, self.y + 40),
                (self.x, self.y + 40 + self.tamano_llama)
            ]
            pygame.draw.polygon(superficie, NARANJA, puntos)
            puntos = [
                (self.x - 4, self.y + 40),
                (self.x + 4, self.y + 40),
                (self.x, self.y + 40 + self.tamano_llama - 10)
            ]
            pygame.draw.polygon(superficie, AMARILLO, puntos)
        
        # Dibujar cohete
        x_pos = self.x + self.desplazamiento_vibracion
        # Cuerpo principal
        pygame.draw.rect(superficie, BLANCO, 
                        (x_pos - 10, self.y - 40, 20, 40))
        # Punta
        pygame.draw.polygon(superficie, ROJO,
                          [(x_pos - 10, self.y - 40),
                           (x_pos + 10, self.y - 40),
                           (x_pos, self.y - 50)])
        # Aletas
        pygame.draw.polygon(superficie, GRIS,
                          [(x_pos - 10, self.y),
                           (x_pos - 20, self.y + 10),
                           (x_pos - 10, self.y - 10)])
        pygame.draw.polygon(superficie, GRIS,
                          [(x_pos + 10, self.y),
                           (x_pos + 20, self.y + 10),
                           (x_pos + 10, self.y - 10)])

class Simulacion:
    def __init__(self):
        # Datos del cohete (ejemplo)
        masa_propelente = [1000, 800, 600]  # kg por etapa
        masa_estructural = [200, 150, 100]   # kg por etapa
        masa_satelite = 100                  # kg
        impulso_especifico = [250, 300, 350] # segundos por etapa
        
        self.cohete = Cohete(masa_propelente, masa_estructural, masa_satelite, impulso_especifico)
        self.ejecutando = True
        self.fondo = NEGRO
        self.estrellas = [(random.randint(0, ANCHO), random.randint(0, ALTO), 
                      random.random()) for _ in range(200)]
        
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.ejecutando = False
    
    def actualizar(self):
        self.cohete.actualizar()
        
    def dibujar(self):
        pantalla.fill(self.fondo)
        
        # Dibujar estrellas con parpadeo
        for i, (x, y, brillo) in enumerate(self.estrellas):
            brillo_actual = brillo * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.001 + i))
            color = (int(255 * brillo_actual),) * 3
            pygame.draw.circle(pantalla, color, (int(x), int(y)), 1)
        
        # Dibujar suelo con degradado
        for i in range(50):
            color = max(0, min(255, 128 - i*2))
            pygame.draw.rect(pantalla, (color, color, color),
                           (0, ALTURA_SUELO + i, ANCHO, 1))
        
        # Dibujar cohete
        self.cohete.dibujar(pantalla)
        
        # Dibujar información
        fuente = pygame.font.Font(None, 36)
        
        if not self.cohete.lanzamiento_iniciado:
            cuenta_atras = f"T-{self.cohete.contador_prelanzamiento//60 + 1}"
            texto_cuenta = fuente.render(cuenta_atras, True, ROJO)
            rect_texto = texto_cuenta.get_rect(center=(ANCHO//2, ALTO//2))
            pantalla.blit(texto_cuenta, rect_texto)
        
        texto_combustible = fuente.render(
            f"Propelente: {int(max(0, self.cohete.masa_propelente[0]))}kg", True, BLANCO)
        texto_altura = fuente.render(
            f"Altura: {int(ALTURA_SUELO - self.cohete.y)}m", True, BLANCO)
        texto_velocidad = fuente.render(
            f"Velocidad: {int(self.cohete.velocidad)}m/s", True, BLANCO)
        
        pantalla.blit(texto_combustible, (10, 10))
        pantalla.blit(texto_altura, (10, 50))
        pantalla.blit(texto_velocidad, (10, 90))
        
        pygame.display.flip()
    
    def ejecutar(self):
        while self.ejecutando:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            reloj.tick(FPS)

if __name__ == "__main__":
    simulacion = Simulacion()
    simulacion.ejecutar()
    pygame.quit()