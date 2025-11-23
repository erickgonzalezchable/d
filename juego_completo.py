"""
🎮 JUEGO DE CARRERAS RETRO 8-BIT - Versión Python Completa
Juego de carreras retro con estética 8-bit, sistema de niveles y multijugador

Controles:
- Jugador 1: Flechas ← →
- Jugador 2: A D

Autor: Convertido de JavaScript a Python con Pygame
"""

# ============================================
# IMPORTACIONES
# ============================================
import pygame
import sys
import json
import os
import time
import random
from datetime import datetime


# ============================================
# CONFIGURACIÓN DEL JUEGO
# ============================================

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Configuración del canvas del juego
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600

# Configuración del jugador
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

# Configuración de enemigos
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 60

# Configuración de la carretera
ROAD_WIDTH = 80
LANES = 3

# Configuración de juego
BASE_SPEED = 3
SPEED_INCREMENT = 0.5
POINTS_PER_CAR = 10
SPEED_UP_EVERY = 10


# ============================================
# NIVELES DE DIFICULTAD
# ============================================
LEVELS = [
    {
        'name': 'FÁCIL',
        'enemy_frequency': 100,
        'max_enemies': 3,
        'min_score': 0
    },
    {
        'name': 'MEDIO',
        'enemy_frequency': 70,
        'max_enemies': 4,
        'min_score': 50
    },
    {
        'name': 'DIFÍCIL',
        'enemy_frequency': 50,
        'max_enemies': 5,
        'min_score': 100
    }
]


# ============================================
# PALETA DE COLORES
# ============================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 51, 0)
GRAY = (51, 51, 51)
DARK_GRAY = (33, 33, 33)


# ============================================
# CONTROLES DE JUGADORES
# ============================================
PLAYER1_CONTROLS = {
    'left': 'left',
    'right': 'right'
}

PLAYER2_CONTROLS = {
    'left': 'a',
    'right': 'd'
}


# ============================================
# CLASE PLAYER
# ============================================

class Player:
    """
    Clase que representa a un jugador en el juego.
    Maneja el movimiento, colisiones, puntuación y renderizado del jugador.
    """
    
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
        self._init_position()
        
        # Estadísticas del jugador
        self._init_stats()
        
        # Enemigos y gestión del juego
        self._init_game_state()
        
        # Controles y apariencia
        self._init_controls_and_appearance()
    
    
    def _init_position(self):
        """Inicializa la posición del jugador"""
        self.x = CANVAS_WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = CANVAS_HEIGHT - PLAYER_HEIGHT - 20
    
    
    def _init_stats(self):
        """Inicializa las estadísticas del jugador"""
        self.score = 0
        self.level = 0
        self.speed = BASE_SPEED
        self.speed_multiplier = 1.0
        self.alive = True
    
    
    def _init_game_state(self):
        """Inicializa el estado del juego para este jugador"""
        self.enemies = []
        self.road_offset = 0
        self.frame_count = 0
        self.passed_enemies = set()
    
    
    def _init_controls_and_appearance(self):
        """Inicializa controles y apariencia del jugador"""
        self.controls = PLAYER1_CONTROLS if self.player_num == 1 else PLAYER2_CONTROLS
        self.color = GREEN if self.player_num == 1 else YELLOW
    
    # ========================================
    # MÉTODOS DE CÁLCULO DE POSICIÓN
    # ========================================
    
    def get_lane_x(self, lane):
        """Obtiene la posición X de un carril específico"""
        lane_width = CANVAS_WIDTH // LANES
        return lane * lane_width + (lane_width - PLAYER_WIDTH) // 2
    
    
    def get_current_lane(self):
        """Obtiene el carril actual del jugador"""
        lane_width = CANVAS_WIDTH // LANES
        return int(self.x // lane_width)
    
    
    # ========================================
    # MÉTODOS DE MOVIMIENTO
    # ========================================
    
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
    
    
    # ========================================
    # MÉTODOS DE GESTIÓN DE ENEMIGOS
    # ========================================
    
    def spawn_enemy(self):
        """Genera un enemigo nuevo según la frecuencia del nivel actual"""
        current_level = LEVELS[self.level]
        
        if (self.frame_count % current_level['enemy_frequency'] == 0 and 
            len(self.enemies) < current_level['max_enemies']):
            
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
            if self._check_enemy_passed(enemy):
                self._handle_enemy_passed(enemy)
            
            # Verificar colisión
            if self.check_collision(enemy):
                self.alive = False
                return True  # Retorna True si hay colisión
            
            # Eliminar enemigos fuera de pantalla
            if self._is_enemy_offscreen(enemy):
                self._remove_enemy(i, enemy)
        
        return False
    
    
    def _check_enemy_passed(self, enemy):
        """Verifica si el jugador adelantó al enemigo"""
        return (enemy['y'] > self.y + PLAYER_HEIGHT and 
                enemy['id'] not in self.passed_enemies)
    
    
    def _handle_enemy_passed(self, enemy):
        """Maneja cuando un enemigo es adelantado"""
        self.passed_enemies.add(enemy['id'])
        self.add_score(POINTS_PER_CAR)
    
    
    def _is_enemy_offscreen(self, enemy):
        """Verifica si el enemigo está fuera de pantalla"""
        return enemy['y'] > CANVAS_HEIGHT
    
    
    def _remove_enemy(self, index, enemy):
        """Elimina un enemigo de la lista"""
        if enemy['id'] in self.passed_enemies:
            self.passed_enemies.remove(enemy['id'])
        self.enemies.pop(index)
    
    
    def check_collision(self, enemy):
        """Verifica si hay colisión entre el jugador y un enemigo"""
        return (self.x < enemy['x'] + ENEMY_WIDTH and
                self.x + PLAYER_WIDTH > enemy['x'] and
                self.y < enemy['y'] + ENEMY_HEIGHT and
                self.y + PLAYER_HEIGHT > enemy['y'])
    
    
    # ========================================
    # MÉTODOS DE PUNTUACIÓN Y NIVELES
    # ========================================
    
    def add_score(self, points):
        """Añade puntos y actualiza la velocidad y nivel"""
        self.score += points
        self._update_speed()
        self._update_level()
    
    
    def _update_speed(self):
        """Actualiza la velocidad según la puntuación"""
        new_speed_multiplier = 1 + (self.score // SPEED_UP_EVERY) * SPEED_INCREMENT
        
        if new_speed_multiplier > self.speed_multiplier:
            self.speed_multiplier = new_speed_multiplier
            self.speed = BASE_SPEED * self.speed_multiplier
    
    
    def _update_level(self):
        """Actualiza el nivel según la puntuación"""
        if self.score >= 100 and self.level < 2:
            self.level = 2
        elif self.score >= 50 and self.level < 1:
            self.level = 1
    
    # ========================================
    # MÉTODOS DE RENDERIZADO
    # ========================================
    
    def draw_road(self, surface):
        """Dibuja la carretera con las líneas de carril"""
        # Fondo de la carretera
        pygame.draw.rect(surface, GRAY, (self.x_offset, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
        
        # Líneas de carril
        self._draw_lane_lines(surface)
        
        # Actualizar desplazamiento de la carretera
        self.road_offset += self.speed
    
    
    def _draw_lane_lines(self, surface):
        """Dibuja las líneas de los carriles"""
        lane_width = CANVAS_WIDTH // LANES
        
        for i in range(1, LANES):
            x = self.x_offset + i * lane_width
            
            # Líneas discontinuas animadas
            for y in range(int(self.road_offset % 40) - 40, CANVAS_HEIGHT, 40):
                pygame.draw.line(surface, WHITE, (x, y), (x, y + 20), 2)
    
    
    def draw_car(self, surface, x, y, color):
        """Dibuja un auto en la posición especificada"""
        x += self.x_offset
        
        # Cuerpo del auto
        pygame.draw.rect(surface, color, (x + 5, y, 30, 50))
        
        # Ventana
        pygame.draw.rect(surface, CYAN, (x + 8, y + 10, 24, 15))
        
        # Ruedas
        self._draw_car_wheels(surface, x, y)
    
    
    def _draw_car_wheels(self, surface, x, y):
        """Dibuja las ruedas del auto"""
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
    
    
    # ========================================
    # MÉTODO DE ACTUALIZACIÓN PRINCIPAL
    # ========================================
    
    def update(self):
        """Actualiza el estado del jugador"""
        if not self.alive:
            return False
        
        self.frame_count += 1
        self.spawn_enemy()
        collision = self.update_enemies()
        
        return not collision  # Retorna True si no hay colisión


# ============================================
# CLASE GAME
# ============================================

class Game:
    """
    Clase principal del juego.
    Maneja el loop principal, menús, controles y renderizado de pantallas.
    """
    
    def __init__(self):
        """Inicializa el juego"""
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Configuración de pantalla
        self._init_display()
        
        # Fuentes
        self._init_fonts()
        
        # Estado del juego
        self._init_game_state()
        
        # Sonidos
        self.load_sounds()
        
        # Archivo de puntuaciones
        self.scores_file = 'scores.json'
    
    
    def _init_display(self):
        """Inicializa la pantalla del juego"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏁 CARRERA RETRO 8-BIT 🏁")
        self.clock = pygame.time.Clock()
    
    
    def _init_fonts(self):
        """Inicializa las fuentes del juego"""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
    
    
    def _init_game_state(self):
        """Inicializa el estado del juego"""
        self.state = 'menu'  # 'menu', 'game', 'scores', 'game_over'
        self.game_mode = 'single'  # 'single' o 'multi'
        self.players = []
    
    # ========================================
    # MÉTODOS DE AUDIO
    # ========================================
    
    def load_sounds(self):
        """Carga los efectos de sonido y música"""
        try:
            # Intenta cargar los sonidos si existen
            if os.path.exists('assets/music.mp3'):
                pygame.mixer.music.load('assets/music.mp3')
                pygame.mixer.music.set_volume(0.3)
            
            self.explosion_sound = None
            self.point_sound = None
            
            if os.path.exists('assets/explosion.mp3'):
                self.explosion_sound = pygame.mixer.Sound('assets/explosion.mp3')
                self.explosion_sound.set_volume(0.5)
            
            if os.path.exists('assets/point.mp3'):
                self.point_sound = pygame.mixer.Sound('assets/point.mp3')
                self.point_sound.set_volume(0.5)
        except:
            print("⚠️ No se pudieron cargar los archivos de audio")
    
    
    def play_music(self):
        """Reproduce la música de fondo"""
        try:
            pygame.mixer.music.play(-1)  # Loop infinito
        except:
            pass
    
    
    def stop_music(self):
        """Detiene la música de fondo"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    
    def play_sound(self, sound):
        """Reproduce un efecto de sonido"""
        try:
            if sound:
                sound.play()
        except:
            pass
    
    
    # ========================================
    # MÉTODOS DE RENDERIZADO DE TEXTO
    # ========================================
    
    def draw_text(self, text, font, color, x, y, center=True):
        """Dibuja texto en la pantalla"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    # ========================================
    # MÉTODOS DE RENDERIZADO DE PANTALLAS
    # ========================================
    
    def draw_menu(self):
        """Dibuja el menú principal"""
        self.screen.fill(BLACK)
        
        # Fondo con efecto de gradiente
        self._draw_gradient_background()
        
        # Título con efecto pulsante
        self._draw_pulsing_title()
        
        # Botones del menú
        self._draw_menu_buttons()
        
        # Instrucciones
        self._draw_instructions()
    
    
    def _draw_gradient_background(self):
        """Dibuja el fondo con efecto de gradiente"""
        for i in range(0, SCREEN_HEIGHT, 20):
            color_val = int(51 * (1 - i / SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, (0, color_val, 0), 
                           (0, i, SCREEN_WIDTH, 20))
    
    
    def _draw_pulsing_title(self):
        """Dibuja el título con efecto pulsante"""
        alpha = int(255 * (0.7 + 0.3 * abs(pygame.time.get_ticks() % 2000 - 1000) / 1000))
        title_color = (0, alpha, 0)
        self.draw_text("🏁 CARRERA RETRO 🏁", self.font_large, title_color, 
                      SCREEN_WIDTH // 2, 80)
    
    
    def _draw_menu_buttons(self):
        """Dibuja los botones del menú principal"""
        button_y = 200
        button_height = 60
        button_spacing = 80
        
        mouse_pos = pygame.mouse.get_pos()
        
        buttons = [
            ("1 JUGADOR", 'single'),
            ("2 JUGADORES", 'multi'),
            ("TOP 3 PUNTAJES", 'scores'),
            ("SALIR", 'quit')
        ]
        
        self.menu_buttons = []
        
        for i, (text, action) in enumerate(buttons):
            y = button_y + i * button_spacing
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y, 400, button_height)
            self.menu_buttons.append((button_rect, action))
            
            # Efecto hover
            self._draw_button(button_rect, text, mouse_pos, button_height)
    
    
    def _draw_button(self, button_rect, text, mouse_pos, button_height):
        """Dibuja un botón individual con efecto hover"""
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, GREEN, button_rect)
            text_color = BLACK
            pygame.draw.rect(self.screen, GREEN, button_rect, 3)
        else:
            pygame.draw.rect(self.screen, DARK_GREEN, button_rect)
            text_color = GREEN
            pygame.draw.rect(self.screen, GREEN, button_rect, 3)
        
        self.draw_text(text, self.font_small, text_color, 
                      button_rect.centerx, button_rect.centery)
    
    
    def _draw_instructions(self):
        """Dibuja las instrucciones del juego"""
        inst_y = SCREEN_HEIGHT - 200
        pygame.draw.rect(self.screen, DARK_GREEN, 
                        (50, inst_y, SCREEN_WIDTH - 100, 150), 2)
        
        self.draw_text("INSTRUCCIONES", self.font_small, GREEN, 
                      SCREEN_WIDTH // 2, inst_y + 20)
        
        instructions = [
            "Jugador 1: ← → (Flechas)",
            "Jugador 2: A D (Teclas)",
            "• 10 pts por adelantar auto • Velocidad aumenta cada 10 pts"
        ]
        
        for i, inst in enumerate(instructions):
            self.draw_text(inst, self.font_tiny, GREEN, 
                          SCREEN_WIDTH // 2, inst_y + 60 + i * 30)
    
    def draw_scores_screen(self):
        """Dibuja la pantalla de puntuaciones"""
        self.screen.fill(BLACK)
        
        # Fondo
        self._draw_gradient_background()
        
        # Título
        self.draw_text("🏆 TOP 3 PUNTAJES 🏆", self.font_large, GREEN, 
                      SCREEN_WIDTH // 2, 80)
        
        # Mostrar puntuaciones
        self._draw_top_scores()
        
        # Botón volver
        self._draw_back_button()
    
    
    def _draw_top_scores(self):
        """Dibuja las mejores puntuaciones"""
        scores = self.get_top_scores()
        
        if scores:
            y = 200
            for i, score in enumerate(scores):
                text = f"{i + 1}. {score['name']} - {score['score']} puntos"
                self.draw_text(text, self.font_medium, GREEN, 
                              SCREEN_WIDTH // 2, y + i * 80)
        else:
            self.draw_text("No hay puntajes registrados", self.font_medium, GREEN, 
                          SCREEN_WIDTH // 2, 300)
    
    
    def _draw_back_button(self):
        """Dibuja el botón de volver"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 120, 300, 60)
        self.back_button = button_rect
        
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, GREEN, button_rect)
            text_color = BLACK
        else:
            pygame.draw.rect(self.screen, DARK_GREEN, button_rect)
            text_color = GREEN
        
        pygame.draw.rect(self.screen, GREEN, button_rect, 3)
        self.draw_text("VOLVER", self.font_small, text_color, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90)
    
    def draw_game(self):
        """Dibuja el juego en progreso"""
        self.screen.fill(BLACK)
        
        # Dibujar información de jugadores
        self._draw_player_info()
        
        # Área de juego
        self._draw_game_area()
    
    
    def _draw_player_info(self):
        """Dibuja la información de los jugadores en la parte superior"""
        info_height = 100
        pygame.draw.rect(self.screen, DARK_GREEN, (0, 0, SCREEN_WIDTH, info_height))
        
        for i, player in enumerate(self.players):
            x = 50 if i == 0 else SCREEN_WIDTH - 250
            y = 20
            
            self.draw_text(f"JUGADOR {player.player_num}", self.font_tiny, GREEN, 
                          x, y, center=False)
            self.draw_text(f"Puntos: {player.score}", self.font_tiny, GREEN, 
                          x, y + 25, center=False)
            self.draw_text(f"Nivel: {LEVELS[player.level]['name']}", self.font_tiny, GREEN, 
                          x, y + 50, center=False)
            self.draw_text(f"Velocidad: {player.speed_multiplier:.1f}x", self.font_tiny, GREEN, 
                          x, y + 75, center=False)
    
    
    def _draw_game_area(self):
        """Dibuja el área de juego con los canvas de los jugadores"""
        info_height = 100
        game_y = info_height + 20
        
        if self.game_mode == 'single':
            self._draw_single_player_canvas(game_y)
        else:
            self._draw_multi_player_canvas(game_y)
    
    
    def _draw_single_player_canvas(self, game_y):
        """Dibuja el canvas para modo un jugador"""
        canvas_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
        game_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        
        self.players[0].x_offset = 0
        self.players[0].draw(game_surface)
        self.screen.blit(game_surface, (canvas_x, game_y))
        
        # Borde del canvas
        pygame.draw.rect(self.screen, GREEN, 
                       (canvas_x - 2, game_y - 2, CANVAS_WIDTH + 4, CANVAS_HEIGHT + 4), 2)
    
    
    def _draw_multi_player_canvas(self, game_y):
        """Dibuja los canvas para modo dos jugadores"""
        spacing = 20
        total_width = CANVAS_WIDTH * 2 + spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, player in enumerate(self.players):
            canvas_x = start_x + i * (CANVAS_WIDTH + spacing)
            game_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
            
            player.x_offset = 0
            player.draw(game_surface)
            self.screen.blit(game_surface, (canvas_x, game_y))
            
            # Borde del canvas
            pygame.draw.rect(self.screen, player.color, 
                           (canvas_x - 2, game_y - 2, CANVAS_WIDTH + 4, CANVAS_HEIGHT + 4), 2)
    
    def draw_game_over(self):
        """Dibuja la pantalla de game over"""
        self.screen.fill(BLACK)
        
        # Fondo semi-transparente
        self._draw_overlay()
        
        # Título
        self.draw_text("¡JUEGO TERMINADO!", self.font_large, RED, 
                      SCREEN_WIDTH // 2, 100)
        
        # Puntuaciones finales
        self._draw_final_scores()
        
        # Botones
        self._draw_game_over_buttons()
    
    
    def _draw_overlay(self):
        """Dibuja una capa semi-transparente"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
    
    
    def _draw_final_scores(self):
        """Dibuja las puntuaciones finales"""
        y = 250
        
        if self.game_mode == 'single':
            self.draw_text(f"Puntuación Final: {self.players[0].score}", 
                          self.font_medium, GREEN, SCREEN_WIDTH // 2, y)
        else:
            for player in self.players:
                self.draw_text(f"Jugador {player.player_num}: {player.score} puntos", 
                              self.font_medium, player.color, SCREEN_WIDTH // 2, y)
                y += 60
    
    
    def _draw_game_over_buttons(self):
        """Dibuja los botones de game over"""
        mouse_pos = pygame.mouse.get_pos()
        button_y = SCREEN_HEIGHT - 200
        
        buttons = [
            ("MENÚ PRINCIPAL", 'menu', button_y),
            ("JUGAR DE NUEVO", 'restart', button_y + 80)
        ]
        
        self.game_over_buttons = []
        
        for text, action, y in buttons:
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y, 400, 60)
            self.game_over_buttons.append((button_rect, action))
            
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, GREEN, button_rect)
                text_color = BLACK
            else:
                pygame.draw.rect(self.screen, DARK_GREEN, button_rect)
                text_color = GREEN
            
            pygame.draw.rect(self.screen, GREEN, button_rect, 3)
            self.draw_text(text, self.font_small, text_color, 
                          SCREEN_WIDTH // 2, y + 30)
    
    
    # ========================================
    # MÉTODOS DE CONTROL DEL JUEGO
    # ========================================
    
    def start_game(self, mode):
        """Inicia un nuevo juego"""
        self.game_mode = mode
        self.state = 'game'
        
        # Crear jugadores
        if mode == 'single':
            self.players = [Player(1, 0)]
        else:
            self.players = [Player(1, 0), Player(2, 0)]
        
        self.play_music()
    
    def update_game(self):
        """Actualiza el estado del juego"""
        all_alive = True
        
        for player in self.players:
            if not player.update():
                all_alive = False
        
        # Si algún jugador murió, game over
        if not all_alive:
            self._handle_game_over()
    
    
    def _handle_game_over(self):
        """Maneja el game over"""
        self.stop_music()
        self.play_sound(self.explosion_sound)
        
        # Guardar puntuaciones
        for player in self.players:
            self.save_score(f"Jugador {player.player_num}", player.score)
        
        self.state = 'game_over'
    
    
    # ========================================
    # MÉTODOS DE MANEJO DE EVENTOS
    # ========================================
    
    def handle_menu_click(self, pos):
        """Maneja clics en el menú principal"""
        for button_rect, action in self.menu_buttons:
            if button_rect.collidepoint(pos):
                if action == 'quit':
                    return False
                elif action == 'scores':
                    self.state = 'scores'
                else:
                    self.start_game(action)
                return True
        return True
    
    
    def handle_scores_click(self, pos):
        """Maneja clics en la pantalla de puntuaciones"""
        if self.back_button.collidepoint(pos):
            self.state = 'menu'
    
    
    def handle_game_over_click(self, pos):
        """Maneja clics en la pantalla de game over"""
        for button_rect, action in self.game_over_buttons:
            if button_rect.collidepoint(pos):
                if action == 'menu':
                    self.state = 'menu'
                    self.stop_music()
                elif action == 'restart':
                    self.start_game(self.game_mode)
    
    
    def handle_controls(self, keys):
        """Maneja los controles de los jugadores"""
        for player in self.players:
            if not player.alive:
                continue
            
            # Detectar pulsaciones de teclas para movimiento
            if player.controls['left'] == 'left' and keys[pygame.K_LEFT]:
                player.move_left()
            elif player.controls['right'] == 'right' and keys[pygame.K_RIGHT]:
                player.move_right()
            elif player.controls['left'] == 'a' and keys[pygame.K_a]:
                player.move_left()
            elif player.controls['right'] == 'd' and keys[pygame.K_d]:
                player.move_right()
    
    
    # ========================================
    # MÉTODOS DE GESTIÓN DE PUNTUACIONES
    # ========================================
    
    def save_score(self, name, score):
        """Guarda una puntuación en el archivo"""
        scores = self.get_top_scores()
        
        scores.append({
            'name': name,
            'score': score,
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        
        scores.sort(key=lambda x: x['score'], reverse=True)
        scores = scores[:3]  # Solo mantener top 3
        
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=2)
    
    
    def get_top_scores(self):
        """Obtiene las mejores puntuaciones"""
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    # ========================================
    # LOOP PRINCIPAL DEL JUEGO
    # ========================================
    
    def run(self):
        """Loop principal del juego"""
        running = True
        keys_pressed = set()
        
        self._print_welcome_message()
        
        while running:
            # Procesar eventos
            running = self._process_events(keys_pressed)
            
            # Actualizar estado
            self._update_state()
            
            # Renderizar
            self._render()
            
            # Mantener FPS
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Salir
        pygame.quit()
        sys.exit()
    
    
    def _print_welcome_message(self):
        """Imprime el mensaje de bienvenida en consola"""
        print("🎮 Juego iniciado correctamente!")
        print("📋 Controles:")
        print("   - Jugador 1: Flechas ← →")
        print("   - Jugador 2: A D")
        print("\n¡Disfruta del juego!\n")
    
    
    def _process_events(self, keys_pressed):
        """Procesa todos los eventos de pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key_down(event.key, keys_pressed)
            
            elif event.type == pygame.KEYUP:
                self._handle_key_up(event.key, keys_pressed)
        
        return True
    
    
    def _handle_mouse_click(self, pos):
        """Maneja los clics del mouse según el estado"""
        if self.state == 'menu':
            return self.handle_menu_click(pos)
        elif self.state == 'scores':
            self.handle_scores_click(pos)
        elif self.state == 'game_over':
            self.handle_game_over_click(pos)
    
    
    def _handle_key_down(self, key, keys_pressed):
        """Maneja cuando se presiona una tecla"""
        if key not in keys_pressed:
            keys_pressed.add(key)
            
            # Control de movimiento al presionar
            if self.state == 'game':
                keys = pygame.key.get_pressed()
                self.handle_controls(keys)
    
    
    def _handle_key_up(self, key, keys_pressed):
        """Maneja cuando se suelta una tecla"""
        if key in keys_pressed:
            keys_pressed.remove(key)
    
    
    def _update_state(self):
        """Actualiza el estado del juego"""
        if self.state == 'game':
            self.update_game()
    
    
    def _render(self):
        """Renderiza la pantalla actual"""
        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'scores':
            self.draw_scores_screen()
        elif self.state == 'game':
            self.draw_game()
        elif self.state == 'game_over':
            self.draw_game_over()


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("🏁 CARRERA RETRO 8-BIT 🏁")
    print("=" * 50)
    game = Game()
    game.run()
