import pygame, sys
from support import *
from settings import *
from entities import Entity
from inventory import Inventory

class Player(Entity):

    def __init__(self, pos, groups, obstacle_sprites, interactive_sprites, enemy_sprites):
        super().__init__(groups)

        #CHARACTER STATES
        self.in_menu = False
        self.in_inventory = False
        self.running = False
        self.attacking = False
        self.attacked = False
        self.recovering = False


        self.inventory = Inventory(self)
        self.inventory.add_item('sword')
        self.inventory.add_item('axe')
        self.inventory.add_item('health_potion')
        self.money = 0

        self.attributes = {
            'Health': 100,
            'Energy': 200,
            'Energy_Recover': 900,
            'Attack': 20,
            'Speed': 200,
        }

        self.spent_energy_time = 0


        #INFOS
        self.sprite_type = 'player'
        self.weapon = 'sword'
        self.weapon_info = items[self.weapon]


        #SPRITE
        self.import_assets()
        self.status = 'down'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center= pos)
        self.z = layers['main']


        #collisions
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(-6, -23)


        #interaction
        self.interactive_sprites = interactive_sprites
        self.enemy_sprites = enemy_sprites

        #movement
        self.speed = self.attributes['Speed']
        self.life = self.attributes['Health']
        self.energy = self.attributes['Energy']

        #attack
        self.attack_time = 0
        self.attack_cooldown = 600


        self.click = False

    def update(self,dt):
        if self.life <= 0:
            self.kill()
            pygame.quit()
            sys.exit()

        self.get_target_pos()

        #COOLDOWN
        self.attacking_cooldown()
        self.energy_recover_cooldown()


        #UPDATES
        self.playerInput()
        self.inventory.update()
        self.get_status()
        self.interact_box()
        self.move(dt)
        self.animate(dt)


    def import_assets(self):
        self.animations = {'left_idle': [], 'right_idle': [], 'down_idle': [],'up_idle': [],
                           'left': [], 'right': [], 'down': [], 'up': [],
                           'left_attacked': [], 'right_attacked': [], 'down_attacked': [], 'up_attacked': [],
                           'left_sword': [], 'right_sword': [], 'down_sword': [], 'up_sword': [],
                           'left_axe': [],'right_axe': [],'down_axe': [],'up_axe': []
                           }

        for animation in self.animations.keys():
            full_path = 'Assets/Sprites/player/' + animation
            self.animations[animation] = import_folder(full_path)

    def get_target_pos(self):
        self.target_pos = self.rect.center + tool_range_offset[self.status.split('_')[0]]

    def playerInput(self):
        keys = pygame.key.get_pressed()
        #move input

        if keys[pygame.K_w]:
            self.status = 'up'
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.status = 'down'
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.status = 'right'
            self.direction.x = 1
        else:
            self.direction.x = 0


        if keys[pygame.K_LSHIFT]:

            if self.energy > 0:
                if self.direction.magnitude() != 0:
                    self.recovering = False
                    self.spent_energy_time = pygame.time.get_ticks()
                    self.running = True
                    self.energy -= 1
            else:
                self.running = False

        else:
            self.running = False


        #INTERACTION KEYS

        if keys[pygame.K_e]:
            for npc in self.interactive_sprites.sprites():
                if npc.rect.collidepoint(self.target_pos):
                    if hasattr(npc, 'sprite_type'):
                        if npc.sprite_type == 'npc':
                            npc.in_chat = True

                        elif npc.sprite_type == 'colletable':
                            if npc.status == 'collect':
                                npc.kill()
                                self.inventory.add_item(npc.name)


        if keys[pygame.K_SPACE] and not self.attacking:
            self.attack()

    def attack(self):
        self.recovering = False
        self.spent_energy_time = pygame.time.get_ticks()


        if self.energy >= self.weapon_info['energy_spent']:
            self.energy -= self.weapon_info['energy_spent']
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

            for enemy in self.enemy_sprites.sprites():
                if enemy.rect.collidepoint(self.target_pos):
                    enemy.damage(self)

            for collect in self.interactive_sprites.sprites():
                if collect.rect.collidepoint(self.target_pos):
                    if hasattr(collect, 'sprite_type') and collect.sprite_type == 'colletable':
                        collect.status = 'collect'

    def attacking_cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False

    def energy_recover_cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.spent_energy_time >= self.attributes['Energy_Recover']:
            self.recovering = True




    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            self.status = f'{self.status.split("_")[0]}_{self.weapon}'

        for sprites in self.groups()[0]:
            if hasattr(sprites, 'sprite_type') and sprites.sprite_type == 'enemy':
                if sprites.attacking:
                    self.status = f'{self.status.split("_")[0]}_attacked'

        if self.running == True:
            self.speed = self.attributes['Speed'] * 2
        else:
            self.speed = self.attributes['Speed']


        if self.recovering == True:
            if self.energy < self.attributes['Energy']:
                self.energy += 1



    def interact_box(self):
        for npc in self.interactive_sprites.sprites():
            if hasattr(npc, 'sprite_type') and npc.sprite_type == 'npc' or npc.sprite_type == 'merchant':
                if npc.rect.collidepoint(self.target_pos):
                    interact_surf = pygame.image.load('Assets/Imagens/overlay/infos/interact.png').convert_alpha()
                    interact_rect = interact_surf.get_rect(topleft = (screen_width-150,screen_height-50))
                    self.display_surface.blit(interact_surf, interact_rect)

        for collect in self.interactive_sprites.sprites():
            if hasattr(collect, 'sprite_type') and collect.sprite_type == 'colletable' or collect.sprite_type == 'dropped':
                if collect.status == 'collect':
                    if collect.rect.colliderect(self.rect):
                        interact_surf = pygame.image.load('Assets/Imagens/overlay/infos/interact.png').convert_alpha()
                        interact_rect = interact_surf.get_rect(topleft = (screen_width-150,screen_height-40))
                        self.display_surface.blit(interact_surf, interact_rect)

















