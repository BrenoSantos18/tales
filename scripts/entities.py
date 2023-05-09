import pygame
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, z = layers['main']):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.z = z
        self.speed = 50

        self.frame_index = 0
        self.direction = pygame.math.Vector2()

    def animate(self,dt):

        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]


    def move(self, dt):
        pos = round(self.speed * dt)


        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * pos
        self.checkCollision('horizontal')
        self.hitbox.y += self.direction.y * pos
        self.checkCollision('vertical')
        self.rect.center = self.hitbox.center


    def checkCollision(self,direction):

        if direction == 'horizontal':
            for obj in self.obstacle_sprites:
                if obj.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = obj.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = obj.hitbox.right


        if direction == 'vertical':
            for obj in self.obstacle_sprites:
                if obj.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = obj.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = obj.hitbox.bottom



