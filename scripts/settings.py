import pygame

#CONFIGS
screen_width = 1000
screen_height = 700
tileSize = 32


tool_range_offset = {
    'left': pygame.math.Vector2(-20,0),
    'right': pygame.math.Vector2(20,0),
    'up': pygame.math.Vector2(0,-30),
    'down': pygame.math.Vector2(0,30),
}


#IMAGENS
map_layouts = {
    'startmap': ['ground', 'scenary objects', 'trees', 'vegetation_obstacles', 'vegetation_objects', 'buildings', 'obstacle', 'upground', 'blocks', 'entities', 'npc', 'merchant','spawn', 'frontier'],
    'playerhouse': ['floor', 'wallpaper', 'furniture', 'top_wall', 'blocks', 'spawn'],
    'passmap': ['ground', 'scenary objects', 'obstacle', 'trees', 'vegetation_obstacles', 'spawn', 'frontier'],
    'cave': ['ground', 'obstacle', 'frontier']
}


layers = {
    'ground': 0,
    'second': 1,
    'main': 2,
    'up': 3
}

#ENTITIES
enemies = {
    'slime': {'health': 5, 'damage': 5, 'detection_area': 360, 'attack_area': 80, 'speed': 50},
    'bear': {'health': 20,  'damage': 10, 'detection_area': 60, 'attack_area': 30, 'speed': 40},
    'thief': {'health': 15,  'damage': 10, 'detection_area': 60, 'attack_area': 30, 'speed': 30},
}





#ITEMS

inventory_types = ['Consumíveis', 'Armas']


items = {
    'sword': {'damage': 20,'value': 10, 'energy_spent': 30, 'type': 'weapon'},
    'axe':{'damage': 10,'value': 10, 'energy_spent': 40, 'type': 'weapon'},
    'stick': {'value': 1, 'type': 'common'},
    'berry': {'value': 1, 'health_restoration': 10, 'type': 'consumable'},
    'health_potion': {'value': 10, 'health_restoration': 60, 'type': 'consumable'},
    'slime': {'value': 5,'type': 'colletable'},
}

merchant_items = {
    'id_1': {
        'sword':{'value': 100, 'amount': 1},
        'axe': {'value': 100, 'amount': 1}
        },
    'id_2': {
        'Espada de Ferro':{},
        'Espada de Aço': {},
        'Armadura': {},
        'Osso': {}
    }
}
