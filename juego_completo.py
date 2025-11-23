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
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
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
POINTS_PER_CAR = 1
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

# Colores adicionales para pieles
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
PURPLE = (200, 0, 255)
PINK = (255, 105, 180)
LIME = (50, 255, 50)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)


# ============================================
# SISTEMA DE PIELES (SKINS)
# ============================================
CAR_SKINS = [
    {
        'name': 'CLÁSICO',
        'body': GREEN,
        'window': CYAN,
        'wheels': BLACK,
        'unlock_score': 0
    },
    {
        'name': 'DEPORTIVO AZUL',
        'body': BLUE,
        'window': WHITE,
        'wheels': BLACK,
        'unlock_score': 500
    },
    {
        'name': 'NARANJA FUEGO',
        'body': ORANGE,
        'window': YELLOW,
        'wheels': BLACK,
        'unlock_score': 500
    },
    {
        'name': 'PÚRPURA NEÓN',
        'body': PURPLE,
        'window': PINK,
        'wheels': BLACK,
        'unlock_score': 500
    },
    {
        'name': 'LIMA ELÉCTRICO',
        'body': LIME,
        'window': YELLOW,
        'wheels': BLACK,
        'unlock_score': 500
    },
    {
        'name': 'CAMPEÓN ORO',
        'body': GOLD,
        'window': WHITE,
        'wheels': BRONZE,
        'unlock_score': 500
    }
]

# Pieles para jugador 2 (modo multijugador)
CAR_SKINS_P2 = [
    {
        'name': 'CLÁSICO',
        'body': YELLOW,
        'window': CYAN,
        'wheels': BLACK,
        'unlock_score': 0
    },
    {
        'name': 'PLATA RACING',
        'body': SILVER,
        'window': CYAN,
        'wheels': BLACK,
        'unlock_score': 500
    },
    {
        'name': 'ROSA NEÓN',
        'body': PINK,
        'window': WHITE,
        'wheels': BLACK,
        'unlock_score': 500
    },
    {
        'name': 'ROJO FERRARI',
        'body': RED,
        'window': BLACK,
        'wheels': DARK_GRAY,
        'unlock_score': 500
    },
    {
        'name': 'AZUL ELÉCTRICO',
        'body': CYAN,
        'window': BLUE,
        'wheels': BLACK,
        'unlock_score': 500
    },
    {
        'name': 'BRONCE CLÁSICO',
        'body': BRONZE,
        'window': ORANGE,
        'wheels': BLACK,
        'unlock_score': 500
    }
]


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
        
        # Sistema de pieles
        self.skins = CAR_SKINS if self.player_num == 1 else CAR_SKINS_P2
        self.current_skin = 0
        self.unlocked_skins = [0]  # Piel 0 siempre desbloqueada
        self.new_skin_unlocked = False
        self.skin_notification = ""
    
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
        old_score = self.score
        self.score += points
        
        # Verificar si se desbloqueó una nueva piel
        self._check_skin_unlock(old_score)
        
        self._update_speed()
        self._update_level()
    
    
    def _check_skin_unlock(self, old_score):
        """Verifica si se desbloqueó una nueva piel"""
        # Verificar cada 500 puntos
        if self.score >= 500 and old_score < 500:
            self._unlock_random_skin()
    
    
    def _unlock_random_skin(self):
        """Desbloquea una piel aleatoria que aún no esté desbloqueada"""
        import random
        
        # Encontrar pieles bloqueadas
        locked_skins = [i for i in range(len(self.skins)) 
                       if i not in self.unlocked_skins and self.skins[i]['unlock_score'] > 0]
        
        if locked_skins:
            new_skin = random.choice(locked_skins)
            self.unlocked_skins.append(new_skin)
            self.current_skin = new_skin
            self.new_skin_unlocked = True
            self.skin_notification = f"¡NUEVA PIEL: {self.skins[new_skin]['name']}!"
    
    
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
        
        # Si es el jugador, usar la piel actual
        if color == self.color:
            skin = self.skins[self.current_skin]
            body_color = skin['body']
            window_color = skin['window']
            wheel_color = skin['wheels']
        else:
            # Para enemigos, usar colores normales
            body_color = color
            window_color = CYAN
            wheel_color = BLACK
        
        # Cuerpo del auto
        pygame.draw.rect(surface, body_color, (x + 5, y, 30, 50))
        
        # Ventana
        pygame.draw.rect(surface, window_color, (x + 8, y + 10, 24, 15))
        
        # Ruedas
        self._draw_car_wheels(surface, x, y, wheel_color)
    
    
    def _draw_car_wheels(self, surface, x, y, wheel_color=BLACK):
        """Dibuja las ruedas del auto"""
        pygame.draw.rect(surface, wheel_color, (x, y + 5, 8, 12))
        pygame.draw.rect(surface, wheel_color, (x + 32, y + 5, 8, 12))
        pygame.draw.rect(surface, wheel_color, (x, y + 33, 8, 12))
        pygame.draw.rect(surface, wheel_color, (x + 32, y + 33, 8, 12))
    
    
    def draw(self, surface):
        """Dibuja todos los elementos del jugador en la pantalla"""
        self.draw_road(surface)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            self.draw_car(surface, enemy['x'], enemy['y'], RED)
        
        # Dibujar jugador si está vivo
        if self.alive:
            self.draw_car(surface, self.x, self.y, self.color)
        
        # Dibujar notificación de nueva piel
        if self.new_skin_unlocked:
            self._draw_skin_notification(surface)
    
    
    def _draw_skin_notification(self, surface):
        """Dibuja la notificación de nueva piel desbloqueada"""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.skin_notification, True, GOLD)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x_offset + CANVAS_WIDTH // 2, 50)
        
        # Fondo semi-transparente
        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pygame.Surface(bg_rect.size)
        bg_surface.set_alpha(200)
        bg_surface.fill(BLACK)
        surface.blit(bg_surface, bg_rect.topleft)
        
        # Texto
        surface.blit(text_surface, text_rect)
    
    
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
        self.fullscreen = False
    
    
    def _init_fonts(self):
        """Inicializa las fuentes del juego"""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
    
    
    def _init_game_state(self):
        """Inicializa el estado del juego"""
        self.state = 'menu'  # 'menu', 'game', 'scores', 'game_over', 'shop'
        self.game_mode = 'single'  # 'single' o 'multi'
        self.players = []
        self.selected_player = 1  # Para la tienda
        self.total_score_p1 = 0
        self.total_score_p2 = 0
    
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
        button_y = 180
        button_height = 55
        button_spacing = 70
        
        mouse_pos = pygame.mouse.get_pos()
        
        buttons = [
            ("1 JUGADOR", 'single'),
            ("2 JUGADORES", 'multi'),
            ("TIENDA DE PIELES", 'shop'),
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
        inst_y = SCREEN_HEIGHT - 180
        pygame.draw.rect(self.screen, DARK_GREEN, 
                        (50, inst_y, SCREEN_WIDTH - 100, 140), 2)
        
        self.draw_text("INSTRUCCIONES", self.font_small, GREEN, 
                      SCREEN_WIDTH // 2, inst_y + 25)
        
        instructions = [
            "Jugador 1: ← → (Flechas)",
            "Jugador 2: A D (Teclas)",
            "• 1 pt por adelantar auto • Velocidad aumenta cada 10 pts"
        ]
        
        for i, inst in enumerate(instructions):
            self.draw_text(inst, self.font_tiny, GREEN, 
                          SCREEN_WIDTH // 2, inst_y + 65 + i * 28)
    
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
            y = 220
            for i, score in enumerate(scores):
                text = f"{i + 1}. {score['name']} - {score['score']} puntos"
                self.draw_text(text, self.font_medium, GREEN, 
                              SCREEN_WIDTH // 2, y + i * 75)
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
    
    
    def draw_shop_screen(self):
        """Dibuja la pantalla de tienda de pieles"""
        self.screen.fill(BLACK)
        
        # Fondo
        self._draw_gradient_background()
        
        # Título
        self.draw_text("🎨 TIENDA DE PIELES 🎨", self.font_large, GREEN, 
                      SCREEN_WIDTH // 2, 60)
        
        # Selector de jugador
        self._draw_player_selector()
        
        # Mostrar puntos acumulados
        total_score = self.total_score_p1 if self.selected_player == 1 else self.total_score_p2
        self.draw_text(f"Puntos Totales: {total_score}", self.font_small, YELLOW, 
                      SCREEN_WIDTH // 2, 140)
        
        # Grid de pieles
        self._draw_skins_grid()
        
        # Botón volver
        self._draw_back_button()
    
    
    def _draw_player_selector(self):
        """Dibuja el selector de jugador"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Botón Jugador 1
        button_p1 = pygame.Rect(SCREEN_WIDTH // 2 - 220, 100, 200, 50)
        self.player_button_1 = button_p1
        
        if self.selected_player == 1:
            pygame.draw.rect(self.screen, GREEN, button_p1)
            text_color = BLACK
        elif button_p1.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, DARK_GREEN, button_p1)
            text_color = GREEN
        else:
            pygame.draw.rect(self.screen, BLACK, button_p1)
            text_color = GREEN
        
        pygame.draw.rect(self.screen, GREEN, button_p1, 3)
        self.draw_text("JUGADOR 1", self.font_tiny, text_color, 
                      SCREEN_WIDTH // 2 - 120, 125)
        
        # Botón Jugador 2
        button_p2 = pygame.Rect(SCREEN_WIDTH // 2 + 20, 100, 200, 50)
        self.player_button_2 = button_p2
        
        if self.selected_player == 2:
            pygame.draw.rect(self.screen, YELLOW, button_p2)
            text_color = BLACK
        elif button_p2.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, DARK_GREEN, button_p2)
            text_color = YELLOW
        else:
            pygame.draw.rect(self.screen, BLACK, button_p2)
            text_color = YELLOW
        
        pygame.draw.rect(self.screen, YELLOW, button_p2, 3)
        self.draw_text("JUGADOR 2", self.font_tiny, text_color, 
                      SCREEN_WIDTH // 2 + 120, 125)
    
    
    def _draw_skins_grid(self):
        """Dibuja la cuadrícula de pieles disponibles"""
        skins = CAR_SKINS if self.selected_player == 1 else CAR_SKINS_P2
        total_score = self.total_score_p1 if self.selected_player == 1 else self.total_score_p2
        
        # Calcular cuántas pieles están desbloqueadas
        unlocked_count = 1  # Siempre tienen la piel clásica
        if total_score >= 500:
            unlocked_count = min(4, 1 + (total_score // 500))  # Máximo 3 pieles adicionales
        
        start_x = 100
        start_y = 200
        skin_width = 150
        skin_height = 200
        spacing = 30
        skins_per_row = 4
        
        self.skin_buttons = []
        
        for i, skin in enumerate(skins):
            row = i // skins_per_row
            col = i % skins_per_row
            
            x = start_x + col * (skin_width + spacing)
            y = start_y + row * (skin_height + spacing)
            
            # Verificar si está desbloqueada
            is_unlocked = i < unlocked_count
            
            # Dibujar tarjeta de piel
            self._draw_skin_card(x, y, skin_width, skin_height, skin, is_unlocked, i)
    
    
    def _draw_skin_card(self, x, y, width, height, skin, is_unlocked, index):
        """Dibuja una tarjeta individual de piel"""
        mouse_pos = pygame.mouse.get_pos()
        card_rect = pygame.Rect(x, y, width, height)
        self.skin_buttons.append((card_rect, index, is_unlocked))
        
        # Fondo de la tarjeta
        if is_unlocked:
            if card_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, DARK_GREEN, card_rect)
            else:
                pygame.draw.rect(self.screen, BLACK, card_rect)
            pygame.draw.rect(self.screen, GREEN, card_rect, 3)
        else:
            pygame.draw.rect(self.screen, DARK_GRAY, card_rect)
            pygame.draw.rect(self.screen, GRAY, card_rect, 3)
        
        # Dibujar mini carro en el centro
        car_x = x + width // 2 - 20
        car_y = y + 50
        self._draw_mini_car(car_x, car_y, skin, is_unlocked)
        
        # Nombre de la piel
        text_y = y + 130
        if is_unlocked:
            self.draw_text(skin['name'], self.font_tiny, skin['body'], 
                          x + width // 2, text_y)
        else:
            self.draw_text(skin['name'], self.font_tiny, GRAY, 
                          x + width // 2, text_y)
        
        # Estado
        status_y = y + height - 30
        if is_unlocked:
            self.draw_text("DESBLOQUEADA", self.font_tiny, GREEN, 
                          x + width // 2, status_y)
        else:
            self.draw_text("🔒 BLOQUEADA", self.font_tiny, RED, 
                          x + width // 2, status_y)
            self.draw_text("500 pts", self.font_tiny, YELLOW, 
                          x + width // 2, status_y + 20)
    
    
    def _draw_mini_car(self, x, y, skin, is_unlocked):
        """Dibuja un mini carro de muestra"""
        scale = 1.5
        
        if is_unlocked:
            body_color = skin['body']
            window_color = skin['window']
            wheel_color = skin['wheels']
        else:
            body_color = GRAY
            window_color = DARK_GRAY
            wheel_color = BLACK
        
        # Cuerpo
        pygame.draw.rect(self.screen, body_color, 
                        (x + 7*scale, y, 45*scale, 75*scale))
        
        # Ventana
        pygame.draw.rect(self.screen, window_color, 
                        (x + 12*scale, y + 15*scale, 36*scale, 22*scale))
        
        # Ruedas
        pygame.draw.rect(self.screen, wheel_color, 
                        (x, y + 7*scale, 12*scale, 18*scale))
        pygame.draw.rect(self.screen, wheel_color, 
                        (x + 48*scale, y + 7*scale, 12*scale, 18*scale))
        pygame.draw.rect(self.screen, wheel_color, 
                        (x, y + 50*scale, 12*scale, 18*scale))
        pygame.draw.rect(self.screen, wheel_color, 
                        (x + 48*scale, y + 50*scale, 12*scale, 18*scale))
    
    def draw_game(self):
        """Dibuja el juego en progreso"""
        self.screen.fill(BLACK)
        
        # Dibujar información de jugadores
        self._draw_player_info()
        
        # Área de juego
        self._draw_game_area()
    
    
    def _draw_player_info(self):
        """Dibuja la información de los jugadores en la parte superior"""
        info_height = 110
        pygame.draw.rect(self.screen, DARK_GREEN, (0, 0, SCREEN_WIDTH, info_height))
        
        for i, player in enumerate(self.players):
            x = 60 if i == 0 else SCREEN_WIDTH - 300
            y = 25
            
            self.draw_text(f"JUGADOR {player.player_num}", self.font_tiny, GREEN, 
                          x, y, center=False)
            self.draw_text(f"Puntos: {player.score}", self.font_tiny, GREEN, 
                          x, y + 28, center=False)
            self.draw_text(f"Nivel: {LEVELS[player.level]['name']}", self.font_tiny, GREEN, 
                          x, y + 56, center=False)
            self.draw_text(f"Velocidad: {player.speed_multiplier:.1f}x", self.font_tiny, GREEN, 
                          x, y + 84, center=False)
            
            # Mostrar piel actual
            skin_name = player.skins[player.current_skin]['name']
            self.draw_text(f"Skin: {skin_name}", self.font_tiny, 
                          player.skins[player.current_skin]['body'], 
                          x, y + 112, center=False)
    
    
    def _draw_game_area(self):
        """Dibuja el área de juego con los canvas de los jugadores"""
        info_height = 140
        game_y = info_height + 15
        
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
        y = 260
        
        if self.game_mode == 'single':
            self.draw_text(f"Puntuación Final: {self.players[0].score}", 
                          self.font_medium, GREEN, SCREEN_WIDTH // 2, y)
        else:
            for player in self.players:
                self.draw_text(f"Jugador {player.player_num}: {player.score} puntos", 
                              self.font_medium, player.color, SCREEN_WIDTH // 2, y)
                y += 55
    
    
    def _draw_game_over_buttons(self):
        """Dibuja los botones de game over"""
        mouse_pos = pygame.mouse.get_pos()
        button_y = SCREEN_HEIGHT - 180
        
        buttons = [
            ("MENÚ PRINCIPAL", 'menu', button_y),
            ("JUGAR DE NUEVO", 'restart', button_y + 75)
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
                elif action == 'shop':
                    self.state = 'shop'
                else:
                    self.start_game(action)
                return True
        return True
    
    
    def handle_shop_click(self, pos):
        """Maneja clics en la tienda de pieles"""
        # Botón volver
        if self.back_button.collidepoint(pos):
            self.state = 'menu'
            return
        
        # Selector de jugador
        if hasattr(self, 'player_button_1') and self.player_button_1.collidepoint(pos):
            self.selected_player = 1
            return
        
        if hasattr(self, 'player_button_2') and self.player_button_2.collidepoint(pos):
            self.selected_player = 2
            return
    
    
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
        # Acumular puntos totales
        if 'Jugador 1' in name:
            self.total_score_p1 += score
        elif 'Jugador 2' in name:
            self.total_score_p2 += score
        
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
    
    
    def toggle_fullscreen(self):
        """Alterna entre pantalla completa y modo ventana"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    
    def _print_welcome_message(self):
        """Imprime el mensaje de bienvenida en consola"""
        print("🎮 Juego iniciado correctamente!")
        print("📋 Controles:")
        print("   - Jugador 1: Flechas ← →")
        print("   - Jugador 2: A D")
        print("   - F11: Pantalla completa")
        print("   - ESC: Volver al menú / Salir")
        print("\n¡Disfruta del juego!\n")
    
    
    def _process_events(self, keys_pressed):
        """Procesa todos los eventos de pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Toggle pantalla completa con F11
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                # Permitir salir con ESC
                elif event.key == pygame.K_ESCAPE:
                    if self.state == 'game':
                        self.state = 'menu'
                        self.stop_music()
                    else:
                        return False
                else:
                    self._handle_key_down(event.key, keys_pressed)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
            
            elif event.type == pygame.KEYUP:
                self._handle_key_up(event.key, keys_pressed)
        
        return True
    
    
    def _handle_mouse_click(self, pos):
        """Maneja los clics del mouse según el estado"""
        if self.state == 'menu':
            return self.handle_menu_click(pos)
        elif self.state == 'scores':
            self.handle_scores_click(pos)
        elif self.state == 'shop':
            self.handle_shop_click(pos)
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
        elif self.state == 'shop':
            self.draw_shop_screen()
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
