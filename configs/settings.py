"""
Parámetros globales: mapa, recursos, tecnologías, estructuras y persistencia.
"""
SETTINGS = {
    "world_size": (1600, 1200),
    "tile_size": 20,
    "initial_tropeles": 5,

    # Terreno
    "water_areas": 10,
    "tree_count": 80,
    "ore_vein_count": 20,

    # Spawn de recursos (ms)
    "resource_spawn_intervals": {
        "food": 15000,
        "wood": 10000,
        "stone": 12000,
        "metal": 20000,
    },

    # Persistencia de alimentos (tiempo de vida en ms)
    "food_ttl": 120000,

    # Necesidades
    "hunger_rate": 0.0015,
    "thirst_rate": 0.0025,
    "hunger_gain": 50,
    "thirst_gain": 70,
    "health_decay_rate": 0.01,

    # Movimiento y comunicación
    "tropel_speed": 70,
    "communication_radius": 120,

    # Árboles: ya en world.trees

    # Esquema de tecnologías (tech tree)
    "technologies": {
        "Stone Tools":   {"requirements": {"stone":5, "wood":2},         "prereqs": []},
        "Fire":          {"requirements": {"wood":5,  "stone":2},       "prereqs": ["Stone Tools"]},
        "Metalworking":  {"requirements": {"metal":5, "stone":3},       "prereqs": ["Stone Tools"]},
        "Agriculture":   {"requirements": {"food":10, "water":5},       "prereqs": ["Fire"]},
        "Electricity":   {"requirements": {"metal":10, "wood":5},       "prereqs": ["Metalworking"]},
    },

    # Estructuras
    "structures": {
        "House":  {"wood":10, "stone":5},
        "Bridge": {"wood":15, "metal":5},
    },

    "tech_speed_bonus": 10,
    "advice_interval": 30000,
    "max_tropeles": 200,
}
