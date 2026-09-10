import math
import pygame

from object_game import ObjectGame

class Enemy(ObjectGame):
    def __init__(self, start_pos, control_pos, target_pos, screen, health=50, damage=20):
        super().__init__(start_pos[0], start_pos[1], screen)
        self.health = health
        self.max_health = health
        self.damage = damage
        self.sprite = pygame.image.load('./assets/enemy/enemy_1_b_m.png')

        # Puntos para la curva Bézier
        self.p0 = start_pos
        self.p1 = control_pos
        self.p2 = target_pos

        self.t = 0.0
        self.speed_t = 0.015
        self.state = "ENTERING"

        # Atributos de Ataque
        self.attack_speed = 7
        self.vx = 0
        self.vy = 0

    def start_attack(self, target_x, target_y):
        """Calcula el vector de dirección hacia la posición actual del jugador."""
        self.state = "ATTACKING"
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.vx = (dx / distance) * self.attack_speed
            self.vy = (dy / distance) * self.attack_speed

    def reenter_formation(self):
        """Reinicia la trayectoria Bézier desde arriba para regresar a su lugar."""
        self.state = "ENTERING"
        self.t = 0.0
        self.p0 = (self.x, -50)  # inicia desde arriba en su X actual

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

    def get_rect(self):
        return self.sprite.get_rect(center=(self.x, self.y))

    def update(self, screen_height=600):
        if self.state == "ENTERING":
            self.t += self.speed_t
            if self.t >= 1.0:
                self.t = 1.0
                self.state = "IN_FORMATION"

            u = 1 - self.t
            self.x = u * u * self.p0[0] + 2 * u * self.t * self.p1[0] + self.t * self.t * self.p2[0]
            self.y = u * u * self.p0[1] + 2 * u * self.t * self.p1[1] + self.t * self.t * self.p2[1]

        elif self.state == "IN_FORMATION":
            self.x += math.sin(pygame.time.get_ticks() * 0.003) * 0.5

        elif self.state == "ATTACKING":
            self.x += self.vx
            self.y += self.vy

            # si el enemigo se pasa del fondo de la pantalla, reingresa por arriba
            if self.y > screen_height + 50:
                self.reenter_formation()

    def draw(self):
        rect = self.sprite.get_rect(center=(self.x, self.y))
        self.screen.blit(self.sprite, rect)
        self.draw_health_bar(rect)

    def draw_health_bar(self, rect):
        # pequeña barra sobre la cabeza del enemigo si ha perdido vida
        if self.health < self.max_health:
            bar_width = 30
            bar_height = 4
            fill = (self.health / self.max_health) * bar_width

            x = rect.centerx - (bar_width // 2)
            y = rect.top - 8

            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_width, bar_height))
            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, fill, bar_height))

