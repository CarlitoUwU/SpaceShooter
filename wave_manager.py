import random
import pygame
from enemy import Enemy
from power_up import PowerUp


class WaveManager:
    def __init__(self, screen, width, players):
        self.screen = screen
        self.width = width
        self.current_wave = 0
        self.score = 0
        self.enemies = []
        self.powerups = []
        self.players = players
        self.revive_timer = 0
        self.revive_duration = 600 # tiempo de espera para revivir
        self.explosion_sound = pygame.mixer.Sound(
            './assets/sounds/explosion.wav')
        self.explosion_sound.set_volume(0.2)
        self.powerup_sound_numbers = {
            'plasma': 1,
            'vulcan': 2,
            'exhaust': 3,
            'proton': 4,
        }
        self.powerup_sounds = {
            number: pygame.mixer.Sound(f'./assets/sounds/powerUp{number}.mp3')
            for number in self.powerup_sound_numbers.values()
        }

        # fuente para el hud
        self.font = pygame.font.SysFont('Arial', 24, bold=True)

        self.attack_cooldown = 120
        self.attack_timer = self.attack_cooldown
        self.bullet_types = ['proton', 'exhaust', 'plasma', 'vulcan']

        self.formations = [
            # 1. Pirámide Clásica (5x3)
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1]
            ],

            # 2. Flecha en "V" (5x3)
            [
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0]
            ],

            # 3. Diamante / Rombo (5x5)
            [
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0]
            ],

            # 4. Alien Invasor Clásico (7x5)
            [
                [0, 0, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [1, 1, 0, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 0]
            ],

            # 5. Formación en "X" / Cruzada (7x5)
            [
                [1, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 1]
            ],

            # 6. Alas de Trinchete / "W" (7x3)
            [
                [1, 0, 1, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 0]
            ],

            # 7. Muralla Pesada con Huecos (7x4)
            [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 1, 0, 0, 0, 1, 1],
                [0, 1, 1, 0, 1, 1, 0]
            ],

            # 8. Punta de Lanza Ancha (7x5)
            [
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 1, 1, 0, 1, 1, 0],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 1]
            ]
        ]

    def trigger_random_attack(self):
        """escoge al enemigo y jugador para hacer el ataque"""
        available_enemies = [
            e for e in self.enemies if e.state == "IN_FORMATION"] # lista de los enemigos en formacion
        available_players = [
            player for player in self.players if player.is_alive] # lista de los jugadores con vida

        if available_enemies and available_players:
            attacker = random.choice(available_enemies)
            target_player = random.choice(available_players)
            player_rect = target_player.get_rect()
            attacker.start_attack(player_rect.centerx, player_rect.centery)

    def spawn_wave(self):
        """spawnea las rondas de enemigos"""
        # selección bucle de rondas para repetir matrices
        formation_idx = self.current_wave % len(self.formations)
        grid = self.formations[formation_idx]

        cell_w, cell_h = 60, 50 # tamaño de las celdas
        start_x = (self.width - (len(grid[0]) * cell_w)) // 2
        start_y = 80

        start_pos = (-50, -50)
        control_pos = (self.width // 2, 400) # segundo punto para la curva

        # escalado de dificultad según la ronda actual
        scaled_health = 50 + (self.current_wave * 5)  # +5 HP por ronda
        scaled_damage = 20 + (self.current_wave * 1)  # +1 Daño por ronda

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    target_x = start_x + (col_idx * cell_w) # posiciones finales
                    target_y = start_y + (row_idx * cell_h)

                    enemy = Enemy(
                        start_pos,
                        control_pos,
                        (target_x, target_y),
                        self.screen,
                        health=scaled_health,
                        damage=scaled_damage
                    )

                    # aumentar la velocidad de movimiento del enemigo ligeramente por ronda
                    enemy.attack_speed = min(12, 6 + (self.current_wave * 0.3))
                    self.enemies.append(enemy)

    def update(self):
        # si no quedan enemigos pasa a la siguiente ronda ilimitadamente
        if not self.enemies:
            self.spawn_wave()
            self.current_wave += 1

        # los ataques se vuelven mas frecuentes segun la ronda
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.trigger_random_attack()
            min_cooldown = max(30, 90 - (self.current_wave * 5))
            max_cooldown = max(60, 180 - (self.current_wave * 10))
            self.attack_timer = random.randint(min_cooldown, max_cooldown)

        for enemy in self.enemies[:]:
            enemy.update()

        for powerup in self.powerups[:]:
            powerup.update()

        self.check_collisions()

    @property
    def is_game_over(self):
        return not any(player.is_alive for player in self.players)

    def handle_revive(self):
        alive_players = [player for player in self.players if player.is_alive]
        dead_players = [
            player for player in self.players if not player.is_alive]

        if not dead_players: # si no hay jugadores muertos
            self.revive_timer = 0
            return

        if not alive_players: # si no hay jugadores vivos
            return

        self.revive_timer += 1
        if self.revive_timer >= self.revive_duration:
            for player in dead_players:
                player.revive()
            self.revive_timer = 0

    def check_collisions(self):
        # balas vs enemigos
        for player in self.players:
            if not player.is_alive:
                continue

            for bullet in player.bullets[:]:
                bullet_rect = bullet.get_rect()
                for enemy in self.enemies[:]:
                    if bullet_rect.colliderect(enemy.get_rect()): # si colisiona la bala con el enemigo
                        if enemy.take_damage(bullet.damage): # si muere el enemigo
                            self.enemies.remove(enemy)
                            self.explosion_sound.play()

                            self.score += 100 * self.current_wave

                            chance = random.randint(0, 10)
                            if chance > 7:
                                random_bullet = random.choice(
                                    self.bullet_types)
                                self.powerups.append(
                                    PowerUp(enemy.x, enemy.y, self.screen, random_bullet))

                        if bullet in player.bullets: # elimina la balla que colisiono
                            player.bullets.remove(bullet)
                        break

        # enemigos vs jugador
        for enemy in self.enemies[:]:
            enemy_rect = enemy.get_rect()
            for player in self.players:
                if player.is_alive and enemy_rect.colliderect(player.get_rect()): # si esta vivo y choca con el enemigo
                    player.take_damage(enemy.damage)
                    self.enemies.remove(enemy) # elimina al enemigo
                    break

        # powerups vs jugador
        for powerup in self.powerups[:]:
            collected = False
            for player in self.players:
                if player.is_alive and player.get_rect().colliderect(powerup.get_rect()): # si choca el powerup
                    player.change_type_bullet(powerup.bullet_type)
                    sound_number = self.powerup_sound_numbers[powerup.bullet_type]
                    self.powerup_sounds[sound_number].play()
                    self.powerups.remove(powerup) # se elimina
                    collected = True
                    break
            if not collected and powerup.y > self.screen.get_height(): # si no fue recolectado y se sale de la pantalla se elimina
                self.powerups.remove(powerup)

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

        for powerup in self.powerups:
            powerup.draw()

        # dibuja el hud
        self.draw_hud()

    def draw_hud(self):
        # texto de score (esquina superior derecha)
        score_surface = self.font.render(
            f"SCORE: {self.score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(self.width - 20, 10))
        self.screen.blit(score_surface, score_rect)

        # texto de ronda actual (esquina superior derecha, debajo del score)
        wave_surface = self.font.render(
            f"RONDA: {self.current_wave}", True, (0, 255, 200))
        wave_rect = wave_surface.get_rect(topright=(self.width - 20, 40))
        self.screen.blit(wave_surface, wave_rect)

        # contador
        if self.revive_timer > 0:
            seconds_left = max(
                1, (self.revive_duration - self.revive_timer + 59) // 60)
            for player in self.players:
                if not player.is_alive:
                    timer_surface = self.font.render(
                        f"REVIVE: {seconds_left}s",
                        True,
                        (255, 220, 0),
                    )
                    timer_x, timer_y = player.hud_position
                    timer_rect = timer_surface.get_rect(
                        midtop=(timer_x + 75, timer_y - 28)
                    )
                    self.screen.blit(timer_surface, timer_rect)
