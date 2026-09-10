import pygame
from object_game import ObjectGame
from bullet import Bullet

class Player(ObjectGame):
    def __init__(self, x, y, color, screen, controls, health=100, hud_position=(10, 10)):
        super().__init__(x, y, screen)
        self.health = health # vida actual
        self.max_health = health # maxima vida
        self.controls = controls # keys para controlar
        self.hud_position = hud_position # posicion de la barra de vida
        self.velocity = [0, 0]  # vector de movimiento
        self.speed = 4 # velocidad
        self.states = ['l2', 'l1', 'm', 'r1', 'r2'] # stados para los sprites
        self.sprites = []
        self.bullets = [] # sus balas del jugador q disparo

        self.current_bullet_type = 'plasma'  # arma por defecto
        self.powerup_timer = 0 # tiempo restante del powerup
        self.shoot_cooldown = 0 # cooldown para volver a disparar
        self.bullet_sound_numbers = { # sonido de las balas
            'plasma': 1,
            'vulcan': 2,
            'exhaust': 3,
            'proton': 4,
        }

        self.laser_sounds = { # cargamos cada sonido archivo
            number: pygame.mixer.Sound(f'./assets/sounds/laser{number}.mp3')
            for number in self.bullet_sound_numbers.values()
        }

        self.death_sound = pygame.mixer.Sound('./assets/sounds/morir.mp3') # muere
        self.revive_sound = pygame.mixer.Sound('./assets/sounds/revivir.mp3') # revive

        # Fuente para mostrar el tiempo del powerup
        self.font = pygame.font.SysFont('Arial', 16, bold=True)

        for state in self.states:
            self.sprites.append(pygame.image.load(f'./assets/player/{color}/player_{state}.png')) # cargamos los sprites

        self.current_state_index = 2 # posicion inicial

    def change_type_bullet(self, new_bullet_type):
        """cambiar el tipo de bala"""
        self.current_bullet_type = new_bullet_type
        if new_bullet_type != 'plasma':
            self.powerup_timer = 1800  # 30s * 60 FPS
        else:
            self.powerup_timer = 0

    def take_damage(self, amount):
        """recibir daño"""
        was_alive = self.is_alive
        self.health = max(0, self.health - amount) # maximo entre 0 y el resto de la vida
        if was_alive and not self.is_alive: # si muere
            self.death_sound.play()

    @property
    def is_alive(self):
        return self.health > 0

    def revive(self):
        self.health = self.max_health
        self.revive_sound.play()

    def get_rect(self):
        current_sprite = self.sprites[self.current_state_index]
        return current_sprite.get_rect(topleft=(self.x, self.y))

    def handle_input(self):
        self.velocity[0] = 0
        self.velocity[1] = 0

        keys = pygame.key.get_pressed()

        if not self.is_alive:
            return

        if keys[self.controls['left']]:
            self.velocity[0] = -self.speed
        if keys[self.controls['right']]:
            self.velocity[0] = self.speed
        if keys[self.controls['up']]:
            self.velocity[1] = -self.speed
        if keys[self.controls['down']]:
            self.velocity[1] = self.speed

        if keys[self.controls['shoot']]:
            self.shoot()

    def shoot(self):
        if self.shoot_cooldown == 0: # si esta en 0 si se puede disparar
            sound_number = self.bullet_sound_numbers[self.current_bullet_type] # del tipo de bala se saca el numero
            self.laser_sounds[sound_number].play() # con el numero sabemos que sonido reproducir
            player_width = self.sprites[self.current_state_index].get_width() # ancho
            center_x = self.x + (player_width // 2)
            bullet_y = self.y

            # plasma 1 bala
            if self.current_bullet_type == 'plasma':
                self.bullets.append(Bullet(
                    center_x, bullet_y, self.screen, angle_degrees=-90, path='plasma', damage=35))
                self.shoot_cooldown = 15 # iniciamos el contador para volver a disparar

            # vulcan 3 balas -105°, -90°, -75°)
            elif self.current_bullet_type == 'vulcan':
                for angle in [-105, -90, -75]:
                    self.bullets.append(Bullet(
                        center_x, bullet_y, self.screen, angle_degrees=angle, path='vulcan', damage=20))
                self.shoot_cooldown = 18

            # exhaust 2 balas una al lado del la otra
            elif self.current_bullet_type == 'exhaust':
                offset = 16 # distancia del centro del sprite (separacion entre las 2 balas)
                self.bullets.append(Bullet(
                    center_x - offset, bullet_y, self.screen, angle_degrees=-90, path='exhaust', damage=18))
                self.bullets.append(Bullet(
                    center_x + offset, bullet_y, self.screen, angle_degrees=-90, path='exhaust', damage=18))
                self.shoot_cooldown = 9

            # proton 4 balas
            elif self.current_bullet_type == 'proton':
                for angle in [-120, -100, -80, -60]:
                    self.bullets.append(Bullet(
                        center_x, bullet_y, self.screen, angle_degrees=angle, path='proton', damage=22))
                self.shoot_cooldown = 22

    def update(self, x_limit, y_limit):
        if not self.is_alive:
            return

        width = self.sprites[self.current_state_index].get_width()
        height = self.sprites[self.current_state_index].get_height()

        new_x = self.x + self.velocity[0]
        new_y = self.y + self.velocity[1]

        self.x = max(0, min(new_x, x_limit - width)) # limites
        self.y = max(0, min(new_y, y_limit - height))

        if self.shoot_cooldown > 0: # si esta en cooldown restamos de 1 en 1
            self.shoot_cooldown -= 1

        # control del temporizador del powerup
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self.current_bullet_type = 'plasma'  # vuelve al arma base

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < -20 or bullet.y > y_limit + 20 or bullet.x < -20 or bullet.x > x_limit + 20: # si se sale de la pantalla lo eliminamos
                self.bullets.remove(bullet)

        # animación de inclinación de la nave
        if self.velocity[0] > 0:
            if self.current_state_index < 4:
                self.current_state_index += 1
        elif self.velocity[0] < 0:
            if self.current_state_index > 0:
                self.current_state_index -= 1
        else:
            if self.current_state_index < 2:
                self.current_state_index += 1
            elif self.current_state_index > 2:
                self.current_state_index -= 1

    def draw(self):
        if not self.is_alive:
            return

        for bullet in self.bullets:
            bullet.draw()

        self.screen.blit(
            self.sprites[self.current_state_index], (self.x, self.y)) # dibuja el player
        self.draw_health_bar() # dibuja la vida

        # muestra los segundos restantes del potenciador sobre la nave
        if self.powerup_timer > 0:
            seconds_left = self.powerup_timer // 60
            timer_text = self.font.render(
                f"{self.current_bullet_type.upper()}: {seconds_left}s", True, (0, 255, 255))
            self.screen.blit(timer_text, (self.x, self.y + 55)) # dibuja el tiempo restante de la bala

    def draw_health_bar(self):
        bar_width = 150
        bar_height = 12
        fill = (self.health / self.max_health) * bar_width
        x, y = self.hud_position
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)

        pygame.draw.rect(self.screen, (255, 0, 0), fill_rect) # relleno
        pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2) # borde
