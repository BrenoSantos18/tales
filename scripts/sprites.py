import pygame, os, sys
from settings import *
from groups import *
from interact import *
from random import randint


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, surface = pygame.Surface((tileSize,tileSize)), z = layers['main']):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.inflate(0,-20)
        self.display_surface = pygame.display.get_surface()


class Building(Tile):
    def __init__(self, pos, group, name, inflate = (0, -40), z = layers['main']):
        super().__init__(pos, group)
        self.building_name = name
        self.inflate = inflate
        self.pos = pos
        self.z = z
        self.status = 'closed'

        self.get_status()


    def update(self, dt):
        self.get_status()

    def get_status(self):
        path = f'Assets/Imagens/buildings/{self.building_name}'
        self.image = pygame.image.load(f'{path}_{self.status}.png')
        self.rect = self.image.get_rect(topleft = self.pos)
        self.hitbox = self.rect.inflate(self.inflate)



class Furniture(Tile):
    def __init__(self, pos, groups, surface, sprite_type = 'none', z = layers['main']):
        super().__init__(pos, groups, surface)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-25)
        self.z = z
        self.sprite_type = sprite_type


class Entry(pygame.sprite.Sprite):
    def __init__(self, pos, groups, name, surface = pygame.Surface((tileSize,tileSize)), z = layers['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        self.name = name


class Interactive(Tile):
    def __init__(self, pos, groups, sprite_type, name, surface=pygame.Surface((tileSize, tileSize)), z=layers['main']):
        super().__init__(pos, groups, surface, z)
        self.sprite_type = sprite_type
        self.name = name
        self.info = interactions[self.name]
        self.in_menu = False
        self.text_index = 0
        self.text_speed = 100
        self.skip_time = 0
        self.skip = False


    def interactive_update(self, player):
        self.can_interact(player)
        if self.in_menu == True:
            self.interaction()



    def can_interact(self, player):
        keys = pygame.key.get_pressed()

        if self.sprite_type == 'interactive_object':
            if self.rect.collidepoint(player.target_pos):
                interact_surf = pygame.image.load('Assets/Imagens/overlay/infos/interact.png').convert_alpha()
                interact_rect = interact_surf.get_rect(topleft = (screen_width-150,screen_height-40))
                self.display_surface.blit(interact_surf, interact_rect)

                if keys[pygame.K_e]:
                    self.in_menu = True




    def interaction(self):
        self.skip_text_cooldown()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.skip:
            self.skip = True
            self.skip_time = pygame.time.get_ticks()
            self.text_index += 1


        amount = max(self.info.keys())

        if self.text_index > amount:
            self.in_menu = False
            self.text_index = 0

        else:
            self.text_box(self.info[self.text_index])


    def skip_text_cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.skip_time >= self.text_speed:
            self.skip = False


    def text_box(self, text):
        font = pygame.font.SysFont(None, 40)

        text_height = (screen_height*35)/100
        text_y = (screen_height*65)/100

        text_bg = pygame.Rect(0,text_y, screen_width, text_height)
        pygame.draw.rect(self.display_surface, 'darkgrey', text_bg)

        text_box = pygame.Rect(15,text_y+10, screen_width-35, text_height-20)
        pygame.draw.rect(self.display_surface, 'white', text_box)

        i = 0

        for lines in text:
            talk_rect = pygame.Rect(20, text_y + 20 + (i * 15),400,80)
            talk = font.render(lines, True, (0,0,0))
            self.display_surface.blit(talk,talk_rect)
            i += 1

class Collect(Tile):
    def __init__(self, pos, group, name, sprite_type = 'vegetation', inflate = (0,0) , z = layers['main']):
        super().__init__(pos, group)
        self.name = name
        self.get_type(sprite_type)
        self.info = items[self.name]
        self.inflate = inflate
        self.get_status(pos)
        self.z = z

    def collect(self):
        for sprites in colletable_sprites:
            if self.status == 'collect':
                sprites.inventory.add_item(self.name)


    def get_status(self, pos):
        if self.sprite_type == 'vegetation':
            path = f'Assets/Imagens/scenary/vegetation/{self.name}'
            self.image = pygame.image.load(f'{path}_{self.status}.png')
            self.rect = self.image.get_rect(center = pos)
            self.hitbox = self.rect.inflate(self.inflate)

        else:
            path = f'Assets/Imagens/items/{self.name}.png'
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect(topleft = pos)


    def get_type(self, sprite_type):
        self.sprite_type = sprite_type

        if self.sprite_type == 'dropped':
            self.status = 'collect'

        if self.sprite_type == 'vegetation':
            self.status = 'normal'








class Vegetation(Tile):
    def __init__(self, pos, group, sprite_type, name, surface=pygame.Surface((tileSize, tileSize)), z=layers['main']):
        super().__init__(pos, group, surface, z)
        self.pos = pos

        self.sprite_type = sprite_type
        self.get_type()
        self.name = name
        if self.name == 'tree':
            self.hitbox = self.rect.inflate((-80, -90))
        self.fruit_sprites = pygame.sprite.Group()

    def update(self, dt):
        self.import_graphic()
        self.create_berry()
        self.get_status()
        self.collect()

    def get_type(self):
        if self.sprite_type == 'colletable':
            self.status = 'normal'

        if self.sprite_type == 'interactive_bush':
            self.has_berry = True
            self.status = 'berries'


    def import_graphic(self):
        if hasattr(self, 'has_berry') or self.sprite_type == 'colletable':

            if self.status == 'collect':
                path = f'Assets/Imagens/scenary/vegetation/{self.name}'
                self.image = pygame.image.load(f'{path}_{self.status}.png')
                self.rect = self.image.get_rect(topleft = self.pos)
            else:
                path = f'Assets/Imagens/scenary/vegetation/{self.name}_{self.status}.png'
                self.image = pygame.image.load(path)




    def create_berry(self):

        if not hasattr(self, 'has_berry'):
            if self.sprite_type == 'collect_bush':
                self.has_berry = True



    def get_status(self):
        if hasattr(self, 'has_berry'):
            if self.has_berry == True:
                self.status = 'berries'

            else:
                self.status = 'no_berries'


    def collect(self):
        for sprites in self.groups()[0]:
            if hasattr(sprites, 'sprite_type')  and sprites.sprite_type == 'player' and hasattr(sprites, 'target_pos'):
                if self.rect.collidepoint(sprites.target_pos):
                    if sprites.attacking == True:
                        if hasattr(self, 'has_berry') and self.has_berry:
                            if sprites.attacking == True:
                                self.has_berry = False
                                sprites.inventory.add_item('berry')
