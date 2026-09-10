# Space Invader

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-00A86B)](https://www.pygame.org/)

Space Invader es un shooter espacial cooperativo para dos jugadores, desarrollado en Python con Pygame. Los jugadores deben sobrevivir a oleadas de enemigos, destruir sus formaciones y aprovechar los power-ups para cambiar temporalmente el tipo de disparo.

## Vista previa

[![Ver el juego en acción](https://img.youtube.com/vi/1QrbjkybGfI/maxresdefault.jpg)](https://youtu.be/1QrbjkybGfI)

También puedes abrir directamente el [video de demostración](https://youtu.be/1QrbjkybGfI).

## Características

- Modo cooperativo local para dos jugadores.
- Oleadas infinitas con ocho formaciones enemigas diferentes.
- Dificultad progresiva: los enemigos ganan vida, daño y velocidad.
- Ataques enemigos dirigidos a los jugadores.
- Cuatro tipos de disparo: `plasma`, `vulcan`, `exhaust` y `proton`.
- Power-ups que caen al derrotar enemigos y duran 30 segundos.
- Barra de vida, puntuación y sistema de reanimación para el jugador derrotado.
- Efectos de sonido, música y sprites para naves, enemigos y proyectiles.

## Controles

| Acción | Jugador 1 | Jugador 2 |
| --- | --- | --- |
| Moverse | `W` `A` `S` `D` | Flechas de dirección |
| Disparar | `Espacio` | `Enter` |

El juego termina cuando los dos jugadores pierden toda su vida. Si uno sigue con vida, el otro puede revivir después de un breve tiempo.

## Instalación

Necesitas Python 3 instalado en el equipo.

1. Clona el repositorio y entra en la carpeta del proyecto:

   ```powershell
   git clone https://github.com/CarlitoUwU/SpaceShooter.git
   cd SpaceShooter
   ```

2. Crea y activa un entorno virtual (recomendado):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

4. Inicia el juego:

   ```powershell
   python main.py
   ```

## Estructura del proyecto

| Archivo o carpeta | Función |
| --- | --- |
| `main.py` | Inicializa Pygame, crea la ventana y ejecuta el bucle principal. |
| `player.py` | Movimiento, vida, disparos, power-ups y controles de cada jugador. |
| `enemy.py` | Entrada en formación, movimiento, ataques y daño de los enemigos. |
| `bullet.py` | Lógica y representación de los proyectiles. |
| `power_up.py` | Power-ups que cambian el tipo de disparo. |
| `wave_manager.py` | Oleadas, formaciones, colisiones, puntuación y reanimación. |
| `object_game.py` | Clase base para los objetos del juego. |
| `assets/` | Sprites, proyectiles, sonidos y demás recursos multimedia. |
| `v1/` | Versión anterior del proyecto. |

## Tecnologías

- Python
- Pygame 2.6.1

## Repositorio

Código fuente: [github.com/CarlitoUwU/SpaceShooter](https://github.com/CarlitoUwU/SpaceShooter)