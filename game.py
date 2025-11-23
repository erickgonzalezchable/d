"""
🎮 JUEGO DE CARRERAS RETRO 8-BIT - Versión Python
Autor: Convertido de JavaScript a Python con Pygame
"""

import pygame
import sys
import json
import os
from datetime import datetime
from player import Player
from config import *


class Game:
    def __init__(self):
        """Inicializa el juego"""
        pygame.init()
        pygame.mixer.init()
        
        # Configuración de pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏁 CARRERA RETRO 8-BIT 🏁")
        self.clock = pygame.time.Clock()
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Estado del juego
        self.state = 'menu'  # 'menu', 'game', 'scores', 'game_over'
        self.game_mode = 'single'  # 'single' o 'multi'
        self.players = []
        
        # Sonidos (opcional - comentado por si no tienes archivos de audio)
        self.load_sounds()
        
        # Archivo de puntuaciones
        self.scores_file = 'scores.json'
    
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
    
    def draw_menu(self):
        """Dibuja el menú principal"""
        self.screen.fill(BLACK)
        
        # Fondo con efecto de gradiente simulado
        for i in range(0, SCREEN_HEIGHT, 20):
            color_val = int(51 * (1 - i / SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, (0, color_val, 0), 
                           (0, i, SCREEN_WIDTH, 20))
        
        # Título con efecto pulsante
        alpha = int(255 * (0.7 + 0.3 * abs(pygame.time.get_ticks() % 2000 - 1000) / 1000))
        title_color = (0, alpha, 0)
        self.draw_text("🏁 CARRERA RETRO 🏁", self.font_large, title_color, 
                      SCREEN_WIDTH // 2, 80)
        
        # Botones del menú
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
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, GREEN, button_rect)
                text_color = BLACK
                pygame.draw.rect(self.screen, GREEN, button_rect, 3)
            else:
                pygame.draw.rect(self.screen, DARK_GREEN, button_rect)
                text_color = GREEN
                pygame.draw.rect(self.screen, GREEN, button_rect, 3)
            
            self.draw_text(text, self.font_small, text_color, 
                          SCREEN_WIDTH // 2, y + button_height // 2)
        
        # Instrucciones
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
        for i in range(0, SCREEN_HEIGHT, 20):
            color_val = int(51 * (1 - i / SCREEN_HEIGHT))
            pygame.draw.rect(self.screen, (0, color_val, 0), 
                           (0, i, SCREEN_WIDTH, 20))
        
        # Título
        self.draw_text("🏆 TOP 3 PUNTAJES 🏆", self.font_large, GREEN, 
                      SCREEN_WIDTH // 2, 80)
        
        # Cargar y mostrar puntuaciones
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
        
        # Botón volver
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
        
        # Área de juego
        game_y = info_height + 20
        
        if self.game_mode == 'single':
            # Un solo canvas centrado
            canvas_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
            game_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
            self.players[0].x_offset = 0
            self.players[0].draw(game_surface)
            self.screen.blit(game_surface, (canvas_x, game_y))
            
            # Borde del canvas
            pygame.draw.rect(self.screen, GREEN, 
                           (canvas_x - 2, game_y - 2, CANVAS_WIDTH + 4, CANVAS_HEIGHT + 4), 2)
        else:
            # Dos canvas lado a lado
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
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Título
        self.draw_text("¡JUEGO TERMINADO!", self.font_large, RED, 
                      SCREEN_WIDTH // 2, 100)
        
        # Puntuaciones finales
        y = 250
        if self.game_mode == 'single':
            self.draw_text(f"Puntuación Final: {self.players[0].score}", 
                          self.font_medium, GREEN, SCREEN_WIDTH // 2, y)
        else:
            for player in self.players:
                self.draw_text(f"Jugador {player.player_num}: {player.score} puntos", 
                              self.font_medium, player.color, SCREEN_WIDTH // 2, y)
                y += 60
        
        # Botones
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
    
    def start_game(self, mode):
        """Inicia un nuevo juego"""
        self.game_mode = mode
        self.state = 'game'
        
        if mode == 'single':
            self.players = [Player(1, 0)]
        else:
            self.players = [Player(1, 0), Player(2, 0)]
        
        self.play_music()
    
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
    
    def update_game(self):
        """Actualiza el estado del juego"""
        all_alive = True
        for player in self.players:
            if not player.update():
                all_alive = False
        
        if not all_alive:
            # Game Over
            self.stop_music()
            self.play_sound(self.explosion_sound)
            
            # Guardar puntuaciones
            for player in self.players:
                self.save_score(f"Jugador {player.player_num}", player.score)
            
            self.state = 'game_over'
    
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
    
    def run(self):
        """Loop principal del juego"""
        running = True
        keys_pressed = set()
        
        while running:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'menu':
                        running = self.handle_menu_click(event.pos)
                    elif self.state == 'scores':
                        self.handle_scores_click(event.pos)
                    elif self.state == 'game_over':
                        self.handle_game_over_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key not in keys_pressed:
                        keys_pressed.add(event.key)
                        # Control de movimiento al presionar
                        if self.state == 'game':
                            keys = pygame.key.get_pressed()
                            self.handle_controls(keys)
                
                elif event.type == pygame.KEYUP:
                    if event.key in keys_pressed:
                        keys_pressed.remove(event.key)
            
            # Actualizar
            if self.state == 'game':
                self.update_game()
            
            # Dibujar
            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'scores':
                self.draw_scores_screen()
            elif self.state == 'game':
                self.draw_game()
            elif self.state == 'game_over':
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
