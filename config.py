"""
Configuración del Juego de Carreras Retro
"""

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

# Niveles de dificultad
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

# Colores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 51, 0)
GRAY = (51, 51, 51)
DARK_GRAY = (33, 33, 33)

# Controles
PLAYER1_CONTROLS = {
    'left': 'left',
    'right': 'right'
}

PLAYER2_CONTROLS = {
    'left': 'a',
    'right': 'd'
}
