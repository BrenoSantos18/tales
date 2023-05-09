
player = {
    'status': {
        'Health': 100,
        'Speed': 200,
        'Damage': 30
    },

    'states': {
        'attacking': False,
        'running': False
    }
}

npc = {
    'Rosalina': {
        'talk': {
            'first interaction': {
                0: ['oi'],
                1: ['Ola']
            },

            'default 1 coração': {
                0: ['eu te conheço'],
                1: ['muito bem']
            },

            'default 1 coração': {
                0: ['eu te conheço ainda mais'],
                1: ['muito bem?']
            },

            'default 1 coração': {
                0: ['eu te conheço muito mais'],
                1: ['muito bem!']
            }
        },

        'status': {
            'talk state': 'first interaction'
        }
    }
}


ground = {
    'South_Valley':{
        'main': 'Assets/Maps/South_Valley/main.png',
        'playerhouse': 'Assets/Maps/South_Valley/playerhouse.png',

    },

    'Castria_West':{
        'main': 'Assets/Maps/Castria_West/main.png',
        'cave': 'Assets/Maps/Castria_West/cave.png'
    }
}

tiled = {
    'South_Valley':{
        'main': 'Assets/Tiled/maps/South_Valley/main.tmx',
        'playerhouse': 'Assets/Tiled/maps/South_Valley/playerhouse.tmx'
    },

    'Castria_West':{
        'main': 'Assets/Tiled/maps/Castria_West/main.tmx',
        'cave': 'Assets/Tiled/maps/Castria_West/cave.tmx'
    }


}


#import_map(mainmap(castria_West, South_Valley), placename(main, cave...))

#types of map_change:

#entries(like houses and caves)
#frontier (south, west,north, east)
