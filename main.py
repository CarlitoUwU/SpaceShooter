import pygame
from player import Player
from wave_manager import WaveManager

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

pygame.mixer.music.load('./assets/sounds/boss.ogg')
pygame.mixer.music.play(-1)

background = pygame.image.load('./assets/fondo.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player1 = Player(
    180,
    500,
    'red',
    screen,
    controls={
        'left': pygame.K_a,
        'right': pygame.K_d,
        'up': pygame.K_w,
        'down': pygame.K_s,
        'shoot': pygame.K_SPACE,
    },
    health=100,
    hud_position=(10, HEIGHT - 30),
)

player2 = Player(
    560,
    500,
    'blue',
    screen,
    controls={
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'shoot': pygame.K_RETURN,
    },
    health=100,
    hud_position=(WIDTH - 160, HEIGHT - 30),
)

wave_manager = WaveManager(screen, WIDTH, [player1, player2])

running = True

while running:
    clock.tick(60) # 60 fps
    screen.fill((0, 0, 0)) # fondo negro inicial
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player1.handle_input()
    player2.handle_input()

    player1.update(WIDTH, HEIGHT)
    player2.update(WIDTH, HEIGHT)

    wave_manager.update()
    wave_manager.handle_revive()

    if wave_manager.is_game_over:
        running = False

    player1.draw()
    player2.draw()
    wave_manager.draw()

    pygame.display.update()
