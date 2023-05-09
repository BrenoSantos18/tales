import pygame
from settings import *
from entities import Entity
from support import *
from npc_support import *

class Npc(Entity):
    def __init__(self, pos, groups, obstacle_sprites, sprite_type = 'npc', name = 'George'):
        super().__init__(groups)


        #VARIABLES
        self.sprite_type = sprite_type
        self.status = 'down_idle'
        self.name = name

        self.texts = npc[self.name]


        self.in_chat = False
        self.situation = 'first_interaction'
        self.chat_index = 0

        #TEXT COOLDOWN
        self.skip_time = 0
        self.text_speed = 100
        self.skip = False


        #GROUPS
        self.obstacle_sprites = obstacle_sprites



        #GRAPHICS
        self.import_graphics(self.name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center= pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.z = layers['main']


        #MOVE
        self.time_index = 1



        self.font = pygame.font.SysFont('arielblack', 30)


    def update(self, dt):
        self.get_status()
        self.animate(dt)
        self.move(dt)
        if self.in_chat == True:
            self.interaction_npc()



    #ANIMATIONS
    def import_graphics(self, name):
        self.animations = {'left_idle':[], 'right_idle':[], 'down_idle':[], 'up_idle':[],
                           'left':[], 'right':[], 'down':[], 'up':[]
                        }

        for animation in self.animations.keys():
            full_path = f'Assets/Sprites/{name}/{animation}'
            self.animations[animation] = import_folder(full_path)


    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.direction.x == -1:
            self.status= 'left'

        elif self.direction.x == 1:
            self.status = 'right'

        elif self.direction.y == -1:
            self.status = 'up'

        elif self.direction.y == 1:
            self.status = 'down'




    def check_time(self, id):
        if id == 1:
            if self.time_index == 1:
                self.move_default()

            elif self.time_index > 20:
                self.time_index = 0

        if id == 2:
            if self.time_index == 1:
                self.move_default()
            elif self.time_index > 120:
                self.time_index = 0

        self.time_index += 1



    #MOVEMENT
    def move_default(self):
        if self.direction.magnitude() == 0:
            self.direction.x = 1

        elif self.direction.x == 1:
            self.direction.x = 0
            self.direction.y = 1

        elif self.direction.y == 1:
            self.direction.y = 0
            self.direction.x = -1

        elif self.direction.x == -1:
            self.direction.x = 0
            self.direction.y = -1

        elif self.direction.y == -1:
            self.direction.y = 0



    #INTERACTION


    def text_box(self, text):
        #cria a caixa e o texto.

        text_height = (screen_height*35)/100
        text_y = (screen_height*65)/100

        text_bg = pygame.Rect(0,text_y, screen_width, text_height)
        pygame.draw.rect(self.display_surface, 'darkgrey', text_bg)

        frame_surf = pygame.image.load('Assets/Imagens/overlay/layout/frame.png').convert_alpha()
        frame_scale = pygame.transform.scale(frame_surf, (192,240))
        frame_rect = frame_surf.get_rect(topleft = (15, text_y))



        text_box = pygame.Rect(15,text_y+10, screen_width-35, text_height-20)
        pygame.draw.rect(self.display_surface, 'white', text_box)

        text_surf = pygame.image.load('Assets/Imagens/overlay/layout/text_box.png').convert_alpha()
        text_rect = text_surf.get_rect(topleft = (212, text_y+20))



        name_surf = self.font.render(self.name, True,(0,0,0))
        name_rect = name_surf.get_rect(center = (15+91, text_y+219))
        self.display_surface.blit(frame_scale,frame_rect)
        self.display_surface.blit(name_surf,name_rect)
        i = 0

        for lines in text:
            talk_rect = pygame.Rect(212, text_y + 25 + (i * 25),400,80)
            talk = self.font.render(lines, True, (0,0,0))
            self.display_surface.blit(talk,talk_rect)
            i += 1





    def interaction_npc(self):
        self.skip_text_cooldown()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.skip:
            self.skip = True
            self.skip_time = pygame.time.get_ticks()
            self.chat_index += 1


        for items in self.texts:

            items = self.situation
            default_value = self.texts[items]

            amount = max(default_value.keys())

            if self.chat_index > amount:
                self.in_chat = False
                self.chat_index = 0

                if self.situation == 'first_interaction':
                    self.situation = 'default'
            else:
                self.text_box(default_value[self.chat_index])


    def skip_text_cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.skip_time >= self.text_speed:
            self.skip = False


class Merchant(Npc):
    def __init__(self, pos, groups, id, obstacle_sprites, sprite_type='merchant', name='merchant'):
        super().__init__(pos, groups, obstacle_sprites, sprite_type, name)
        self.id = merchant_items[id]
        self.status = 'down_idle'
        self.z = layers['main']
        self.interact = False
        self.first_interaction = False
        self.amount_of_items = 0
        self.bought = False




    def show_market(self):
        mouse, _, __ = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()



        market_bg = pygame.Rect((screen_width/2)-400,(screen_height/2)-325,800,650)
        pygame.draw.rect(self.display_surface, 'black', market_bg)
        for item,_ in self.id.items():
            slot_bg = pygame.Rect((screen_width/2)-380 + self.amount_of_items * 100 + self.amount_of_items * 30,(screen_height/2)-305,100,100)
            pygame.draw.rect(self.display_surface, 'blue', slot_bg)

            if self.id[item]['amount'] > 0:
                item_surf = pygame.image.load(f'Assets/Imagens/items/{item}.png')
                item_scale = pygame.transform.scale(item_surf, (90,90))
                item_slot = item_surf.get_rect(topleft = ((screen_width/2)-370 + self.amount_of_items * 100 + self.amount_of_items * 30,(screen_height/2)-295))
                self.display_surface.blit(item_scale, item_slot)

                if slot_bg.collidepoint((mx,my)):
                    if mouse:
                        if self.bought == False:
                            self.bought = True
                            for groups in self.groups()[0]:
                                if hasattr(groups, 'sprite_type') and groups.sprite_type == 'player':
                                        if groups.money >= self.id[item]['value']:
                                            print('oi')
                                            groups.money -= self.id[item]['value']
                                            self.id[item]['amount'] -= 1
                                            groups.add_item(item)

                    else:
                        self.bought = False

            else:
                item_surf = pygame.image.load(f'Assets/Imagens/items/sold_out.png')
                item_slot = item_surf.get_rect(topleft = ((screen_width/2)-380 + self.amount_of_items * 100 + self.amount_of_items * 30,(screen_height/2)-305))
                self.display_surface.blit(item_surf, item_slot)





            self.amount_of_items += 1

        self.amount_of_items = 0




