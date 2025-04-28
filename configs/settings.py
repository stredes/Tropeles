# tropeles_game/configs/settings.py

"""
Parámetros globales mejorados con agricultura dinámica y construcción estratégica.
"""
SETTINGS = {
    # Pantalla
    "world_size":          (1980, 1080),
    "tile_size":           20,
    "initial_tropeles":    5,

    # Terreno
    "water_areas":         10,
    "tree_count":          80,
    "ore_vein_count":      20,
    "farmland_count":      30,

    # Agricultura / Construcción
    "agriculture_interval": 60000,   # ms entre plantaciones de árboles
    "farm_interval":        120000,  # ms entre creación de granjas
    "house_interval":       180000,  # ms entre construcción de casas

    # Animales
    "initial_animals":      15,
    "animal_speed":         50,
    "animal_spawn_interval":20000,

    # Recursos & TTL
    "resource_spawn_intervals": {
        "food":  10000,  # manzanas frecuentes
        "wood":  10000,
        "stone": 12000,
        "metal": 20000,
        "crop":  15000,
        "ore":   15000,
        "meat":  0,
    },
    "food_ttl":  None,       # manzanas no caducan
    "crop_ttl":  180000,     # cultivos duran 3m
    "ore_ttl":   300000,

    # Necesidades
    "hunger_rate":        0.001,
    "thirst_rate":        0.002,
    "hunger_gain":        50,
    "thirst_gain":        70,
    "meat_gain":          80,
    "health_decay_rate":  0.01,

    # Movimiento / Comunicación
    "tropel_speed":         70,
    "communication_radius": 120,

    # Tech-tree
    "technologies": {
        "Stone Tools":   {"requirements":{"stone":5,"wood":2},    "prereqs":[]},
        "Fire":          {"requirements":{"wood":5,"stone":2},    "prereqs":["Stone Tools"]},
        "Agriculture":   {"requirements":{"crop":10},             "prereqs":["Fire"]},
        "Mining":        {"requirements":{"ore":10},              "prereqs":["Stone Tools"]},
        "Metalworking":  {"requirements":{"metal":5,"stone":3},    "prereqs":["Mining"]},
        "Electricity":   {"requirements":{"metal":10,"wood":5},   "prereqs":["Metalworking"]},
    },

    # Estructuras
    "structures": {
        "House":  {"wood":10,"stone":5},
        "Bridge": {"wood":15,"metal":5},
    },

    # Bonos / Límites
    "tech_speed_bonus": 10,
    "advice_interval":  30000,
    "max_tropeles":     200,
}
