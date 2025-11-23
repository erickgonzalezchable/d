"""
Clase Player para el Juego de Carreras Retro
"""

import pygame
import time
from config import *


class Player:
    def __init__(self, player_num, x_offset=0):
        """
        Inicializa un jugador
        
        Args:
            player_num: Número del jugador (1 o 2)
            x_offset: Desplazamiento horizontal para modo multijugador
        """
        self.player_num = player_num
        self.x_offset = x_offset
        
        # Posición inicial del jugador
        self.x = CANVAS_WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = CANVAS_HEIGHT - PLAYER_HEIGHT - 20
        
        # Estadísticas del jugador
        self.score = 0
        self.level = 0
        self.speed = BASE_SPEED
        self.speed_multiplier = 1.0
        self.alive = True
        
        # Enemigos y gestión del juego
        self.enemies = []
        self.road_offset = 0
        self.frame_count = 0
        self.passed_enemies = set()
        
        # Controles
        self.controls = PLAYER1_CONTROLS if player_num == 1 else PLAYER2_CONTROLS
        
        # Color del auto del jugador
        self.color = GREEN if player_num == 1 else YELLOW
    
    def get_lane_x(self, lane):
        """Obtiene la posición X de un carril específico"""
        lane_width = CANVAS_WIDTH // LANES
        return lane * lane_width + (lane_width - PLAYER_WIDTH) // 2
    
    def get_current_lane(self):
        """Obtiene el carril actual del jugador"""
        lane_width = CANVAS_WIDTH // LANES
        return int(self.x // lane_width)
    
    def move_left(self):
        """Mueve el jugador al carril izquierdo"""
        current_lane = self.get_current_lane()
        if current_lane > 0:
            self.x = self.get_lane_x(current_lane - 1)
    
    def move_right(self):
        """Mueve el jugador al carril derecho"""
        current_lane = self.get_current_lane()
        if current_lane < LANES - 1:
            self.x = self.get_lane_x(current_lane + 1)
    
    def spawn_enemy(self):
        """Genera un enemigo nuevo según la frecuencia del nivel actual"""
        current_level = LEVELS[self.level]
        if (self.frame_count % current_level['enemy_frequency'] == 0 and 
            len(self.enemies) < current_level['max_enemies']):
            import random
            lane = random.randint(0, LANES - 1)
            enemy_id = time.time() + random.random()
            self.enemies.append({
                'x': self.get_lane_x(lane),
                'y': -ENEMY_HEIGHT,
                'id': enemy_id
            })
    
    def update_enemies(self):
        """Actualiza la posición de los enemigos y verifica colisiones"""
        for i in range(len(self.enemies) - 1, -1, -1):
            enemy = self.enemies[i]
            enemy['y'] += self.speed
            
            # Verificar si el jugador adelantó al enemigo
            if (enemy['y'] > self.y + PLAYER_HEIGHT and 
                enemy['id'] not in self.passed_enemies):
                self.passed_enemies.add(enemy['id'])
                self.add_score(POINTS_PER_CAR)
            
            # Verificar colisión
            if self.check_collision(enemy):
                self.alive = False
                return True  # Retorna True si hay colisión
            
            # Eliminar enemigos fuera de pantalla
            if enemy['y'] > CANVAS_HEIGHT:
                if enemy['id'] in self.passed_enemies:
                    self.passed_enemies.remove(enemy['id'])
                self.enemies.pop(i)
        
        return False
    
    def check_collision(self, enemy):
        """Verifica si hay colisión entre el jugador y un enemigo"""
        return (self.x < enemy['x'] + ENEMY_WIDTH and
                self.x + PLAYER_WIDTH > enemy['x'] and
                self.y < enemy['y'] + ENEMY_HEIGHT and
                self.y + PLAYER_HEIGHT > enemy['y'])
    
    def add_score(self, points):
        """Añade puntos y actualiza la velocidad y nivel"""
        self.score += points
        
        # Actualizar velocidad cada SPEED_UP_EVERY puntos
        new_speed_multiplier = 1 + (self.score // SPEED_UP_EVERY) * SPEED_INCREMENT
        if new_speed_multiplier > self.speed_multiplier:
            self.speed_multiplier = new_speed_multiplier
            self.speed = BASE_SPEED * self.speed_multiplier
        
        # Cambiar nivel según puntos
        if self.score >= 100 and self.level < 2:
            self.level = 2
        elif self.score >= 50 and self.level < 1:
            self.level = 1
    
    def draw_road(self, surface):
        """Dibuja la carretera con las líneas de carril"""
        # Fondo de la carretera
        pygame.draw.rect(surface, GRAY, (self.x_offset, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
        
        # Líneas de carril
        lane_width = CANVAS_WIDTH // LANES
        for i in range(1, LANES):
            x = self.x_offset + i * lane_width
            # Líneas discontinuas animadas
            for y in range(int(self.road_offset % 40) - 40, CANVAS_HEIGHT, 40):
                pygame.draw.line(surface, WHITE, (x, y), (x, y + 20), 2)
        
        self.road_offset += self.speed
    
    def draw_car(self, surface, x, y, color):
        """Dibuja un auto en la posición especificada"""
        x += self.x_offset
        
        # Cuerpo del auto
        pygame.draw.rect(surface, color, (x + 5, y, 30, 50))
        
        # Ventana
        pygame.draw.rect(surface, CYAN, (x + 8, y + 10, 24, 15))
        
        # Ruedas
        pygame.draw.rect(surface, BLACK, (x, y + 5, 8, 12))
        pygame.draw.rect(surface, BLACK, (x + 32, y + 5, 8, 12))
        pygame.draw.rect(surface, BLACK, (x, y + 33, 8, 12))
        pygame.draw.rect(surface, BLACK, (x + 32, y + 33, 8, 12))
    
    def draw(self, surface):
        """Dibuja todos los elementos del jugador en la pantalla"""
        self.draw_road(surface)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            self.draw_car(surface, enemy['x'], enemy['y'], RED)
        
        # Dibujar jugador si está vivo
        if self.alive:
            self.draw_car(surface, self.x, self.y, self.color)
    
    def update(self):
        """Actualiza el estado del jugador"""
        if not self.alive:
            return False
        
        self.frame_count += 1
        self.spawn_enemy()
        collision = self.update_enemies()
        
        return not collision  # Retorna True si no hay colisión
