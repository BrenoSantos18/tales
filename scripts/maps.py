import pygame, sys, os
from player import Player
from sprites import *
from settings import *
from groups import *
from pytmx.util_pygame import load_pygame
from random import choice
from camera import CameraGroup
from ui import UI
from npc import *
from enemies import Enemy


#Class that deals with whats displaying on the screen.

class Level:
    def __init__(self):

        #Screen
        self.display_surface = pygame.display.get_surface()
        self.actual_place = 'startmap'
        self.last_place = 'none'
        self.came_from = 'none'
        self.start = True


        #Groups and objects
        self.draw_map('none')
        self.start = True

        self.ui = UI(self.player)



    #display on the screen
    def draw(self, dt):
        self.display_surface.fill('black')

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(dt)

        for sprite in self.interactive_sprites.sprites():
            if hasattr(sprite, 'sprite_type'):
                if sprite.sprite_type == 'interactive_object':
                    sprite.interactive_update(self.player)



        for enemy in self.enemy_sprites.sprites():
            enemy.enemy_update(dt, self.player)

        self.ui.update_ui(self.player)
        self.see_collisions()


    #drawing stuff
    def destroy_map(self):
        groups = [
        self.obstacle_sprites,
        self.interactive_sprites,
        self.npc_sprites,
        self.door_sprites,
        self.frontier_sprites,
        self.enemy_sprites
        ]

        for group in groups:
            for sprites in group:
                sprites.kill()



    def draw_map(self, came_from):
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interactive_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.frontier_sprites = pygame.sprite.Group()



        map = self.actual_place
        tmx_data = load_pygame('Assets/Tiled/maps/' + map + '.tmx')

        Tile(
            pos = (0,0),
            group = [self.visible_sprites],
            surface = pygame.image.load(f'Assets/Imagens/scenary/maps/{map}/{map}.png').convert(),
            z = layers['ground'])

        for layout in map_layouts[map]:

            #PLAYER
            if layout == 'spawn':
                for obj in tmx_data.get_layer_by_name('spawn'):
                    if self.actual_place == 'startmap':
                        if obj.type == 'spawn':
                            if self.start == False:
                                self.player= Player((obj.x,obj.y),self.visible_sprites, self.obstacle_sprites,self.interactive_sprites, self.enemy_sprites)

                            elif self.start == True:
                                if came_from == 'east':
                                    if obj.name == 'spawn_east':
                                        self.player= Player((obj.x,obj.y),self.visible_sprites, self.obstacle_sprites,self.interactive_sprites, self.enemy_sprites)

                                else:
                                    if obj.name == 'playerhouse':
                                        self.player= Player((obj.x,obj.y),self.visible_sprites, self.obstacle_sprites,self.interactive_sprites, self.enemy_sprites)

                    if self.actual_place == 'playerhouse':
                        self.player= Player((obj.x,obj.y),self.visible_sprites, self.obstacle_sprites,self.interactive_sprites, self.enemy_sprites)

                    if self.actual_place == 'passmap':
                        if came_from == 'west':
                            if obj.name == 'spawn_west':
                                self.player= Player((obj.x,obj.y),self.visible_sprites, self.obstacle_sprites,self.interactive_sprites, self.enemy_sprites)

            #TILES

            if layout == 'obstacle':
                for x,y, surface in tmx_data.get_layer_by_name('obstacle').tiles():
                    Tile((x * tileSize,y * tileSize), [obstacle_sprites], surface)


            #OBJECTS
            if layout == 'vegetation_objects':
                for obj in tmx_data.get_layer_by_name('vegetation_objects'):
                    Vegetation((obj.x, obj.y), [self.visible_sprites, obstacle_sprites, self.interactive_sprites], obj.type, obj.name, obj.image)

            if layout == 'upground':
                for x,y,surface in tmx_data.get_layer_by_name('upground').tiles():
                    Tile(
                    pos = (x * tileSize, y * tileSize),
                    group = self.visible_sprites,
                    surface = surface,
                    z = layers['up'])


            if layout == 'buildings':
                for obj in tmx_data.get_layer_by_name('buildings'):
                    Building((obj.x,obj.y), [self.visible_sprites, self.obstacle_sprites], obj.name)

            if layout == 'wallpaper':
                for x,y,surface in tmx_data.get_layer_by_name('wallpaper').tiles():
                    Tile(
                    pos = (x * tileSize,y * tileSize),
                    group = [self.obstacle_sprites, self.visible_sprites],
                    surface = surface,
                    z = layers['second'])

            if layout == 'furniture':
                for obj in tmx_data.get_layer_by_name('furniture'):
                    if obj.type == 'interactive_object':
                        if obj.name == 'bed':
                            Interactive(pos = (obj.x,obj.y),
                                        groups = [self.visible_sprites, self.interactive_sprites],
                                        sprite_type = obj.type,
                                        name = obj.name,
                                        surface = obj.image,
                                        z = layers['second'])

                        else:
                            Interactive(pos = (obj.x,obj.y),
                                        groups = [self.visible_sprites, obstacle_sprites, self.interactive_sprites],
                                        sprite_type = obj.type,
                                        name = obj.name,
                                        surface = obj.image,
                                        z = layers['main'])

                    else:
                        Furniture((obj.x,obj.y), [self.visible_sprites, obstacle_sprites], obj.image, obj.name)



            if layout == 'top_wall':
                for x,y,surface in tmx_data.get_layer_by_name('top_wall').tiles():
                    Tile(
                    pos = (x * tileSize,y * tileSize),
                    group = [self.obstacle_sprites, self.visible_sprites],
                    surface = surface)


            #LIVING THINGS
            if layout == 'npc':
                for obj in tmx_data.get_layer_by_name('npcs'):
                    Npc((obj.x,obj.y), [self.visible_sprites, self.npc_sprites, self.interactive_sprites], self.obstacle_sprites, obj.type, obj.name)

            if layout == 'entities':
                for obj in tmx_data.get_layer_by_name('entities'):
                    if obj.type == 'enemy':
                        Enemy((obj.x,obj.y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, obj.name)




            if layout == 'frontier':
                for obj in tmx_data.get_layer_by_name('frontier'):
                    if obj.type == 'pass_north':
                        if self.actual_place == 'startmap':
                            Entry((obj.x,obj.y), [self.frontier_sprites], 'none', obj.image)

                    if obj.type == 'pass_south':

                        Entry((obj.x,obj.y), self.frontier_sprites, 'pass_south')

                    if obj.type == 'pass_west':
                        Entry((obj.x,obj.y), self.frontier_sprites, obj.name, obj.image)

                    if obj.type == 'pass_east':
                        Entry((obj.x,obj.y), [self.frontier_sprites], obj.name, obj.image)


            if layout == 'blocks':
                for obj in tmx_data.get_layer_by_name('blocks'):
                    if obj.type == 'way_in':
                        if obj.name == 'playerhouse_door':
                            Entry((obj.x,obj.y), self.door_sprites, 'playerhouse_door')

                    if obj.type == 'way_out':
                        if obj.name == 'playerhouse_door_out':
                            Entry((obj.x,obj.y), self.door_sprites, 'playerhouse_door_out')

                        if obj.name == 'cave':
                            Entry((obj.x,obj.y), self.door_sprites, 'cave')





    #COLLISION

    def see_collisions(self):
        self.door_collision()
        self.frontier_collisions()


    def door_collision(self):

        #CHANGE THE SPRITE OF THE BUILDINGS
        for building in self.visible_sprites:
            if hasattr(building, 'building_name'):
                if building.rect.collidepoint(self.player.target_pos):
                    if building.status == 'closed':
                        building.status = 'open'
                else:
                    building.status = 'closed'

        for sprites in self.door_sprites.sprites():
            if sprites.rect.collidepoint(self.player.target_pos):

                interact_surf = pygame.image.load('Assets/Imagens/overlay/infos/interact.png').convert_alpha()
                interact_rect = interact_surf.get_rect(topleft = (screen_width-150,screen_height-40))
                self.display_surface.blit(interact_surf, interact_rect)

                keys = pygame.key.get_pressed()

                if keys[pygame.K_e]:
                    self.destroy_map()
                    if self.actual_place == 'startmap':
                        if sprites.name == 'playerhouse_door':
                            self.actual_place = 'playerhouse'
                            self.draw_map('none')

                    elif self.actual_place == 'playerhouse':
                        if sprites.name == 'playerhouse_door_out':
                            self.actual_place = 'startmap'
                            self.draw_map('none')

    def frontier_collisions(self):
        for sprites in self.frontier_sprites.sprites():
            if sprites.rect.colliderect(self.player.hitbox):
                if sprites.name == 'passmap':
                    if self.actual_place == 'startmap':
                        self.destroy_map()
                        self.came_from = 'west'
                        self.actual_place = 'passmap'
                        self.draw_map(self.came_from)

                if sprites.name == 'startmap':
                    if self.actual_place == 'passmap':
                        self.destroy_map()
                        self.came_from = 'east'
                        self.actual_place = 'startmap'
                        self.draw_map(self.came_from)





