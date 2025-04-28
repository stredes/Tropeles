import random
from entities.resource   import Resource
from entities.technology import Technology

class World:
    """Genera terreno, recursos persistentes y tecnologías."""
    def __init__(self, config):
        self.config      = config
        self.width, self.height = config["world_size"]
        self.tile_size   = config["tile_size"]
        self.grid_w      = self.width  // self.tile_size
        self.grid_h      = self.height // self.tile_size

        self.water_tiles = set()
        self.trees       = []
        self.ore_veins   = []

        self.resources   = []
        self.tropeles    = []
        self.techs       = []

        self._generate_water(config["water_areas"])
        self._generate_trees(config["tree_count"])
        self._generate_ore_veins(config["ore_vein_count"])

        for name, info in config["technologies"].items():
            self.techs.append(
                Technology(name, info["requirements"], info["prereqs"])
            )

        self.spawn_timers = {k: 0 for k in config["resource_spawn_intervals"]}

    def _generate_water(self, count):
        for _ in range(count):
            x0 = random.randint(0, self.grid_w - 5)
            y0 = random.randint(0, self.grid_h - 5)
            w, h = random.randint(3,7), random.randint(3,7)
            for i in range(x0, x0 + w):
                for j in range(y0, y0 + h):
                    self.water_tiles.add((i, j))

    def _generate_trees(self, count):
        for _ in range(count):
            while True:
                i, j = random.randint(0, self.grid_w-1), random.randint(0,self.grid_h-1)
                if (i,j) not in self.water_tiles:
                    self.trees.append((i, j))
                    break

    def _generate_ore_veins(self, count):
        for _ in range(count):
            i, j = random.randint(0,self.grid_w-1), random.randint(0,self.grid_h-1)
            self.ore_veins.append((i, j))

    def add_tropel(self, tropel):
        self.tropeles.append(tropel)

    def update(self, dt):
        # 1) Generar recursos
        for kind, interval in self.config["resource_spawn_intervals"].items():
            self.spawn_timers[kind] += dt
            if self.spawn_timers[kind] >= interval:
                self.spawn_timers[kind] %= interval
                self._spawn_resource(kind)

        # 2) Actualizar recursos (ttl) y tropeles
        self.resources = [
            r for r in self.resources if r.update(dt)
        ]

        new_borns = []
        for t in list(self.tropeles):
            child = t.update(dt)
            if child:
                new_borns.append(child)
        for c in new_borns:
            self.add_tropel(c)

        # 3) Filtrar tropeles muertos
        self.tropeles = [t for t in self.tropeles if t.alive]

    def _spawn_resource(self, kind):
        ttl = None
        if kind == "food":
            ttl = self.config["food_ttl"]
        if kind == "food":
            for (i,j) in self.trees:
                if random.random() < 0.5:
                    x = i*self.tile_size + self.tile_size//2
                    y = j*self.tile_size + self.tile_size//2
                    self.resources.append(Resource("food", (x,y), amount=1, ttl=ttl))
        elif kind == "wood":
            i,j = random.choice(self.trees)
            x = i*self.tile_size + random.randint(-5,5)
            y = j*self.tile_size + random.randint(-5,5)
            self.resources.append(Resource("wood",(x,y),1))
        elif kind == "stone":
            i,j = random.choice(self.ore_veins)
            x = i*self.tile_size + random.randint(-8,8)
            y = j*self.tile_size + random.randint(-8,8)
            self.resources.append(Resource("stone",(x,y),1))
        elif kind == "metal":
            i,j = random.choice(self.ore_veins)
            x = i*self.tile_size + random.randint(-8,8)
            y = j*self.tile_size + random.randint(-8,8)
            self.resources.append(Resource("metal",(x,y),1))
