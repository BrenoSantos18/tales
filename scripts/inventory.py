import pygame
from settings import *


class Inventory:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.infos = False
        self.in_inventory = False
        self.list = 0
        self.my_inventory = {}
        self.player = player
        self.menu = 0

        self.click = False


        self.text_font = pygame.font.SysFont('arielblack', 20)
        self.number_font = pygame.font.SysFont(None, 15)


    def update(self):
        self.get_player_input()
        self.show_inventory()



    def get_player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_TAB]:
            self.in_inventory = True



    def show_inventory(self):
        if self.in_inventory == True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False

            mx, my = pygame.mouse.get_pos()


            inventory_bg = pygame.Rect(screen_width-300,(screen_height/2)-200,300,400)
            pygame.draw.rect(self.display_surface, 'brown', inventory_bg)

            close_button = pygame.Rect(screen_width-20,(screen_height/2)-210,20,20)
            pygame.draw.rect(self.display_surface, 'white', close_button)

            if self.menu == 0:
                menu_type_surf = pygame.image.load('Assets/Imagens/overlay/layout/inventory/weapon_rect.png')


            if self.menu == 1:
                menu_type_surf = pygame.image.load('Assets/Imagens/overlay/layout/inventory/consumable_rect.png')

            menu_type_rect = menu_type_surf.get_rect(topleft = (screen_width-200 ,screen_height/2-184))
            self.display_surface.blit(menu_type_surf, menu_type_rect)

            right_arrow = pygame.image.load('Assets/Imagens/overlay/layout/inventory/right.png')
            left_arrow = pygame.image.load('Assets/Imagens/overlay/layout/inventory/left.png')
            right_arrow_rect = right_arrow.get_rect(topleft = (screen_width-90 ,screen_height/2-190))
            left_arrow_rect = left_arrow.get_rect(topleft = (screen_width-228 ,screen_height/2-190))
            self.display_surface.blit(right_arrow, right_arrow_rect)
            self.display_surface.blit(left_arrow, left_arrow_rect)

            if right_arrow_rect.collidepoint((mx, my)):
                if not self.menu == 1:
                    if self.click:
                        self.menu += 1

            if left_arrow_rect.collidepoint((mx, my)):
                if not self.menu == 0:
                    if self.click:
                        self.menu -= 1

            for item,_ in self.my_inventory.items():
                if self.my_inventory[item]['amount'] > 0:
                    if self.menu == 0:
                        item_type = 'weapon'

                    elif self.menu == 1:
                        item_type = 'consumable'


                    if self.my_inventory[item]['type'] == item_type:
                        pos = ((screen_width-300)+(self.list * 10)+(self.list*30)+10, (screen_height/2)-200 + 50)

                        slot_surf = pygame.image.load('Assets/Imagens/overlay/layout/inventory_square.png')
                        slot_rect = slot_surf.get_rect(topleft= pos)


                        text = self.number_font.render(f'{self.my_inventory[item]["amount"]}', True, (0,0,0))
                        text_rect = text.get_rect(center = (pos[0]+32,pos[1]+32) )

                        self.display_surface.blit(slot_surf, slot_rect)

                        item_image = pygame.image.load(f'Assets/Imagens/items/{item}.png')
                        item_rect = item_image.get_rect(topleft = (pos[0]+4,pos[1]+ 4))
                        self.display_surface.blit(item_image, item_rect)
                        self.display_surface.blit(text, text_rect)


                        if slot_rect.collidepoint(mx, my) and self.click:
                            self.infos = True

                        if self.infos == True:
                            if self.my_inventory[item]['type'] == 'weapon':
                                bind_surf = pygame.Surface((60,20))
                                bind_surf.fill('grey')
                                bind_rect = bind_surf.get_rect(topleft = (pos[0],pos[1]+30))
                                new_text = self.text_font.render(f'Equip',True, 'black')
                                new_text_rect = new_text.get_rect(topleft = (pos[0] + 5,pos[1] + 35))
                                self.display_surface.blit(bind_surf, bind_rect)
                                self.display_surface.blit(new_text, new_text_rect)

                                if bind_rect.collidepoint((mx, my)) and self.click:
                                    self.player.weapon = item

                            if self.my_inventory[item]['type'] == 'consumable':
                                use_surf = pygame.Surface((100,10))
                                use_surf.fill('yellow')
                                use_rect = use_surf.get_rect(topleft = (pos[0],pos[1] + 30))
                                new_text = self.text_font.render(f'Usar',True, 'black')
                                new_text_rect = new_text.get_rect(topleft = (pos[0] + 5,pos[1] + 35))
                                self.display_surface.blit(use_surf, use_rect)
                                self.display_surface.blit(new_text, new_text_rect)
                                if use_rect.collidepoint(mx, my) and self.click:
                                    self.use_item()

                    self.list += 1
            self.list = 0

            #COLLISIONS
            if close_button.collidepoint(mx, my):
                pygame.draw.rect(self.display_surface, 'grey', close_button)
                if self.click == True:
                    if self.in_inventory == True:
                        self.in_inventory = False
                        if self.infos == True:
                            self.infos = False



    def add_item(self, name):
        if name in self.my_inventory:
            self.my_inventory[name]['amount'] += 1
            self.my_inventory[name]['value'] += items[name]['value']

        else:
            self.my_inventory[name] = items[name]
            self.my_inventory[name]['amount'] = 1


    def use_item(self):
        for items in self.my_inventory.items():
            for item in items[1]:
                if item == 'health_restoration':
                    if self.player.life + self.my_inventory[items[0]]['health_restoration'] > self.player.attributes['Health'] and not self.player.life == self.player.attributes['Health']:
                        self.player.life = self.player.attributes['Health']
                        self.my_inventory[items[0]]['amount'] -= 1
                    elif self.player.life < self.player.attributes['Health']:
                        self.player.life += self.my_inventory[items[0]]['health_restoration']
                        self.my_inventory[items[0]]['amount'] -= 1




















