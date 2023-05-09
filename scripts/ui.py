import pygame
from settings import *


class UI:
    def __init__(self, player):
        super().__init__()
        self.overlay_sprite = pygame.sprite.Group()

        self.display_screen = pygame.display.get_surface()
        self.actual_tool = 'sword'
        self.life_overlay = pygame.image.load('Assets/Imagens/overlay/infos/life.png')
        self.life_rect = self.life_overlay.get_rect(topleft = (10,10))
        self.energy_overlay = pygame.image.load('Assets/Imagens/overlay/infos/energy.png')
        self.energy_rect = self.energy_overlay.get_rect(topleft = (10,40))

        self.health_bar_rect = pygame.rect.Rect(25,10,190,22)
        self.energy_bar_rect = pygame.rect.Rect(15,40,290,18)
        self.player = player


    def set_overlay_tool(self):
        path = 'Assets/Imagens/overlay/tools/'
        self.overlay_image = pygame.image.load(path + self.actual_tool + '.png')
        self.overlay_scale = pygame.transform.scale(self.overlay_image, (50,50))
        self.overlay_rect = self.overlay_image.get_rect(topleft = (20, screen_height-70))
        self.display_screen.blit(self.overlay_scale, self.overlay_rect)

    def change_tool(self):
        self.actual_tool = self.player.weapon


    def update_ui(self, player):
        self.change_tool()
        self.show_bar(player.life, player.attributes['Health'], self.health_bar_rect, 'red', player.energy, player.attributes['Energy'], self.energy_bar_rect)
        self.display_screen.blit(self.life_overlay, self.life_rect)
        self.display_screen.blit(self.energy_overlay, self.energy_rect)



    def show_bar(self, current, max, bg_rect, color, current_energy, max_energy, energy_bg):
        self.set_overlay_tool()

        #energy
        energy_ratio = current_energy / max_energy
        energy_current_width = energy_bg.width * energy_ratio
        energy_current_rect = energy_bg.copy()
        energy_current_rect.width = energy_current_width

        pygame.draw.rect(self.display_screen, 'black', energy_bg)
        pygame.draw.rect(self.display_screen, 'blue', energy_current_rect)

        #life
        ratio = current / max
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_screen, 'black', bg_rect)
        pygame.draw.rect(self.display_screen, color, current_rect)





