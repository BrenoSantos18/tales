from entities import Entity
from support import *
from settings import *
from groups import *
from sprites import Collect


class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, name, sprite_type = 'enemy'):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.name = name
        self.obstacle_sprites = obstacle_sprites
        self.import_graphics(self.name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0,-16)
        self.enemy_info = enemies[self.name]
        self.speed = self.enemy_info['speed']
        self.life = self.enemy_info['health']
        self.attack_time = 0
        self.attack_cooldown = 600
        self.attacking = False


    def enemy_update(self, dt, player):
        self.get_status(player)
        self.attacking_cooldown()
        self.actions(player)
        self.animate(dt)
        self.move(dt)

    def actions(self, player):
        if self.status == 'attack':
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack(player)


        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]

        else:
            self.direction = pygame.math.Vector2()


    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[]
                        }

        for animation in self.animations.keys():
            full_path = f'Assets/Sprites/enemy/{name}/{animation}'
            self.animations[animation] = import_folder(full_path)


    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 20:
            direction = (player_vec - enemy_vec).normalize()

        else:
            direction = pygame.math.Vector2()

        return(distance, direction)



    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.enemy_info['attack_area'] and not self.attacking:
            self.status = 'attack'

        elif distance <= self.enemy_info['detection_area']:
            self.status = 'move'

        else:
            self.status = 'idle'


    def attacking_cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False




    def damage(self, player):
        total_damage = player.attributes['Attack'] + player.weapon_info['damage']
        self.life -= total_damage
        print(total_damage)
        if self.life <= 0:
            self.kill()

    def attack(self, player):
        player.life -= self.enemy_info['damage']
