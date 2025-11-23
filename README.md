# 🎮 JUEGO DE CARRERAS RETRO 8-BIT

Un emocionante juego de carreras retro con estética 8-bit, sistema de niveles, multijugador y efectos de sonido.

**🐍 Ahora disponible en Python con Pygame!**

## ✨ Características

### Funcionalidades Principales
- ✅ **3 Niveles de Dificultad**: Fácil, Medio y Difícil
- ✅ **Sistema de Puntuación**: 10 puntos por cada auto adelantado
- ✅ **Incremento de Velocidad**: Aumenta cada 10 puntos
- ✅ **Efectos Visuales**: Explosiones animadas en colisiones
- ✅ **Sistema de Audio**: Música de fondo y efectos de sonido (opcional)
- ✅ **Top 3 Puntajes**: Guarda y muestra los mejores puntajes
- ✅ **Modo Multijugador**: Pantalla dividida para 2 jugadores

## 🎮 Controles

### Jugador 1
- **←** (Flecha Izquierda): Mover a la izquierda
- **→** (Flecha Derecha): Mover a la derecha

### Jugador 2 (Modo Multijugador)
- **A**: Mover a la izquierda
- **D**: Mover a la derecha

## 🚀 Cómo Jugar

### Versión Python (Recomendada)

1. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecuta el juego**:
   ```bash
   python game.py
   ```

3. **Selecciona** modo de juego:
   - **1 Jugador**: Juega solo y compite por el mejor puntaje
   - **2 Jugadores**: Juega con un amigo en pantalla dividida
   - **Top 3 Puntajes**: Revisa los mejores puntajes guardados

4. **Esquiva** los autos enemigos (rojos)
5. **Adelanta** autos para ganar puntos
6. **Sobrevive** lo más posible mientras la velocidad aumenta

### Versión Web (HTML/JavaScript)

1. **Abre** el archivo `index.html` en tu navegador
2. Sigue los pasos 3-6 de arriba

## 📊 Sistema de Puntuación

- **10 puntos** por cada auto adelantado
- La **velocidad aumenta** automáticamente cada 10 puntos
- **3 niveles** que se desbloquean según puntos:
  - **Nivel 1 (Fácil)**: 0-49 puntos
  - **Nivel 2 (Medio)**: 50-99 puntos
  - **Nivel 3 (Difícil)**: 100+ puntos

## 🎵 Audio

El juego incluye soporte para:
- **Música de fondo** durante el juego
- **Efecto de explosión** al colisionar
- **Efecto de puntos** al adelantar autos

### Agregar Archivos de Audio (Opcional)

Para que el audio funcione completamente, agrega los siguientes archivos MP3 en la carpeta `assets/`:

1. `music.mp3` - Música de fondo (puedes usar música retro 8-bit)
2. `explosion.mp3` - Sonido de explosión
3. `point.mp3` - Sonido al ganar puntos

El juego funcionará perfectamente sin estos archivos, simplemente sin audio.

**Recursos gratuitos recomendados:**
- [Freesound.org](https://freesound.org/) - Efectos de sonido gratuitos
- [OpenGameArt.org](https://opengameart.org/) - Música y efectos para juegos
- [ZapSplat](https://www.zapsplat.com/) - Biblioteca de sonidos gratuitos

## 📁 Estructura del Proyecto

```
juego/
├── game.py             # 🐍 Juego principal Python (ejecutar este)
├── player.py           # 🐍 Clase del jugador
├── config.py           # 🐍 Configuración del juego
├── requirements.txt    # 🐍 Dependencias Python
├── scores.json         # Puntuaciones guardadas (se genera automáticamente)
├── index.html          # Versión web HTML
├── styles.css          # Versión web CSS
├── game.js             # Versión web JavaScript
├── assets/             # Carpeta para archivos de audio (opcional)
│   ├── music.mp3       # Música de fondo (agregar)
│   ├── explosion.mp3   # Efecto de explosión (agregar)
│   └── point.mp3       # Efecto de puntos (agregar)
└── README.md           # Este archivo
```

## 🔧 Características Técnicas

### Versión Python
- **Pygame** para renderizado y gestión de eventos
- **JSON** para guardar puntajes
- **Sistema de colisiones** preciso
- **Múltiples niveles de dificultad** dinámicos
- **60 FPS** para movimiento fluido

### Versión Web
- **Canvas HTML5** para renderizado
- **LocalStorage** para guardar puntajes
- **Diseño responsivo** con estética retro
- **Animaciones CSS** para efectos visuales
- **Sistema de colisiones** preciso
- **Múltiples niveles de dificultad** dinámicos

## 🎨 Personalización

### Python
Puedes modificar fácilmente las constantes en `config.py`:

```python
# Configuración de juego
BASE_SPEED = 3              # Velocidad inicial
SPEED_INCREMENT = 0.5       # Incremento de velocidad
POINTS_PER_CAR = 10         # Puntos por auto
SPEED_UP_EVERY = 10         # Cada cuántos puntos aumenta velocidad
LANES = 3                   # Número de carriles
```

### JavaScript
Puedes modificar fácilmente las constantes en `game.js`:

```javascript
const CONFIG = {
    canvasWidth: 400,          // Ancho del canvas
    canvasHeight: 600,         // Alto del canvas
    baseSpeed: 3,              // Velocidad inicial
    speedIncrement: 0.5,       // Incremento de velocidad
    pointsPerCar: 10,          // Puntos por auto
    speedUpEvery: 10,          // Cada cuántos puntos aumenta velocidad
    // ... más opciones
};
```

## 🐛 Solución de Problemas

### Versión Python

**Error: No module named 'pygame'**
```bash
pip install pygame
```

**El juego va muy rápido/lento**
- Ajusta `BASE_SPEED` y `FPS` en `config.py`

**Los controles no responden**
- Asegúrate de que la ventana del juego tenga foco
- Verifica que estés usando las teclas correctas

### Versión Web

**El audio no funciona**
- Algunos navegadores bloquean el audio automático. Interactúa con la página primero.
- Asegúrate de que los archivos MP3 estén en la carpeta `assets/`

**El juego va muy rápido/lento**
- Ajusta `baseSpeed` y `speedIncrement` en el archivo `game.js`

**Los controles no responden**
- Asegúrate de que el navegador tenga foco en la ventana del juego
- Verifica que estés usando las teclas correctas

## 📝 Notas

- El juego guarda automáticamente el **Top 3** de puntajes en el navegador
- Los archivos de audio son opcionales, el juego funciona sin ellos
- Compatible con navegadores modernos (Chrome, Firefox, Edge, Safari)

## 🎯 Objetivos del Juego

1. Sobrevivir el mayor tiempo posible
2. Ganar la mayor cantidad de puntos
3. Llegar al nivel 3 (Difícil)
4. Entrar en el Top 3 de puntajes
5. ¡Derrotar a tu amigo en modo multijugador!

---

**¡Disfruta del juego y que gane el mejor piloto! 🏁**

jskdhkajhsdjkhasd
