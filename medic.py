import pygame
import random

class Medic(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("images/medic.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.speed = pygame.math.Vector2(0, 6)
        self.rect.center = pos

    def update(self, size):
        self.rect.move_ip(self.speed)

        if self.rect.top < 1:
            self.speed[1] *= -1
            self.rect.top = 1
        elif self.rect.bottom > size[1]:
            self.speed[1] *= -1
            self.rect.bottom = size[1] - 1
        
        if self.rect.left < 1:
            self.speed[0] *= -1
            self.rect.left = 1
        elif self.rect.right > size[0]:
            self.speed[0] *= -1
            self.rect.right = size[0] - 1
        
        if random.randint(0, 20) == 0:
            rotation = random.choice([-15, 15])
            self.speed.rotate_ip(rotation)