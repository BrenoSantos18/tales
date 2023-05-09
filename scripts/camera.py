import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2((0,0))


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - screen_width /2
        self.offset.y = player.rect.centery - screen_height /2

        for layer in layers.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    #if sprite == player:
                     #       pygame.draw.rect(self.display_surface,'red',offset_rect,5)
                      #      hitbox_rect = player.hitbox.copy()
                       #     hitbox_rect.center = offset_rect.center
                         #   pygame.draw.rect(self.display_surface,'green',hitbox_rect, 5)
                         #   target_pos = offset_rect.center + tool_range_offset[player.status.split('_')[0]]
                        #    pygame.draw.circle(self.display_surface,'blue',target_pos, 5)
