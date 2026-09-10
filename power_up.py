import pygame
from object_game import ObjectGame

class PowerUp(ObjectGame):
    def __init__(self, x, y, screen, bullet_type):
        super().__init__(x, y, screen)
        self.bullet_type = bullet_type

        # carga dinámica según el tipo 'proton', 'exhaust', 'plasma', 'vulcan'
        self.sprite = pygame.image.load(f'./assets/powerups/{self.bullet_type}_bullet.png')
        self.velocity_y = 3

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))

    def update(self):
        self.y += self.velocity_y

    def get_rect(self):
        return self.sprite.get_rect(topleft=(self.x, self.y))