import math
import os
import pygame
from object_game import ObjectGame

class Bullet(ObjectGame):
    def __init__(self, x, y, screen, angle_degrees=0, path='vulcan', damage=25):
        super().__init__(x, y, screen)
        self.angle = angle_degrees
        self.speed = 10
        self.damage = damage
        self.sprites = []

        bullet_folder = f'./assets/bullet/{path}'
        files = [file for file in os.listdir(bullet_folder) if file.endswith('.png')]
        files.sort(key=lambda file: int(os.path.splitext(file)[0]))

        for file_name in files:
            image_path = os.path.join(bullet_folder, file_name)
            base_sprite = pygame.image.load(image_path)
            rotated_sprite = pygame.transform.rotate(base_sprite, -self.angle - 90)
            self.sprites.append(rotated_sprite)

        rad = math.radians(self.angle)
        self.vx = self.speed * math.cos(rad)
        self.vy = self.speed * math.sin(rad)

        self.index_sprite = 0.0
        self.animation_speed = 0.2

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.index_sprite = (self.index_sprite + self.animation_speed) % len(self.sprites)

    def draw(self):
        current_sprite = self.sprites[int(self.index_sprite)]
        rect = current_sprite.get_rect(center=(self.x, self.y))
        self.screen.blit(current_sprite, rect)

    def get_rect(self):
        current_sprite = self.sprites[int(self.index_sprite)]
        return current_sprite.get_rect(center=(self.x, self.y))
