# tropeles_game/entities/tropel.py

import math
import random
from pygame.math import Vector2
from ai.ollama_client       import query
from entities.resource      import Resource

class Tropel:
    REPRO_THRESHOLD = 95
    REPRO_COOLDOWN  = 60000

    def __init__(self, world, ai_client=query):
        self.world         = world
        self.ai            = ai_client
        cfg                = world.config

        cx, cy             = world.width//2, world.height//2
        self.pos          = Vector2(cx, cy)
        self.speed        = cfg["tropel_speed"]
        self.hunger       = 100.0
        self.thirst       = 100.0
        self.health       = 100.0
        self.alive        = True
        self.comm_radius  = cfg["communication_radius"]

        # Inventario dinámico
        self.inventory    = {k:0 for k in cfg["resource_spawn_intervals"].keys()}
        self.known_tech   = set()

        # Agricultura / construcción cooldowns
        self.agri_timer   = cfg["agriculture_interval"]
        self.farm_timer   = cfg["farm_interval"]
        self.house_timer  = cfg["house_interval"]
        self.repro_timer  = 0
        self.advice_timer = cfg["advice_interval"]

    def think(self):
        cfg = self.world.config

        # Beber
        if self.thirst < self.hunger and self.world.water_tiles:
            return self._find_nearest_water()

        # Comer (food, crop, meat)
        if self.hunger < 50:
            foods = [r for r in self.world.resources if r.kind in ("food","crop","meat")]
            if foods:
                return self._find_nearest_resource(foods)

        # Cazar si carne baja
        if self.inventory["meat"] < 2 and self.world.animals:
            nearest = min(self.world.animals, key=lambda a: self.pos.distance_to(a.pos))
            return Vector2(nearest.pos)

        # Recolectar
        for kind in self.inventory:
            if kind not in ("food","crop","meat") and self.inventory[kind] < 5:
                res = [r for r in self.world.resources if r.kind==kind]
                if res:
                    return self._find_nearest_resource(res)

        # Investigar
        for tech in self.world.techs:
            if tech.name not in self.known_tech and tech.can_research(self):
                return None

        # Plantar árbol si agrícola listo
        if "Agriculture" in self.known_tech and self.agri_timer==0 and self.inventory["food"]>=5:
            return None

        # Crear granja si agrícola y farm_timer listo
        if "Agriculture" in self.known_tech and self.farm_timer==0 and self.inventory["wood"]>=10:
            return None

        # Construir casa si estructura lista
        if self.house_timer==0 and self.inventory["wood"]>=10 and self.inventory["stone"]>=5:
            return None

        return None

    def _find_nearest_water(self):
        best = min(self.world.water_tiles,
                   key=lambda t: (self.pos.x/self.world.tile_size - t[0])**2
                               +(self.pos.y/self.world.tile_size - t[1])**2)
        x = best[0]*self.world.tile_size + self.world.tile_size//2
        y = best[1]*self.world.tile_size + self.world.tile_size//2
        return Vector2(x,y)

    def _find_nearest_resource(self, resources):
        res = min(resources, key=lambda r: self.pos.distance_to(r.position))
        return Vector2(res.position)

    def update(self, dt):
        cfg = self.world.config
        if not self.alive:
            return None

        # Timers
        self.repro_timer  = max(0, self.repro_timer  - dt)
        self.advice_timer = max(0, self.advice_timer - dt)
        self.agri_timer   = max(0, self.agri_timer   - dt)
        self.farm_timer   = max(0, self.farm_timer   - dt)
        self.house_timer  = max(0, self.house_timer  - dt)

        # Hambre/Thirst clamp
        self.hunger = max(0, self.hunger - cfg["hunger_rate"] * dt)
        self.thirst = max(0, self.thirst - cfg["thirst_rate"] * dt)

        # Beber
        tx,ty = int(self.pos.x//cfg["tile_size"]), int(self.pos.y//cfg["tile_size"])
        if (tx,ty) in self.world.water_tiles:
            self.thirst = min(100, self.thirst + cfg["thirst_gain"]*(dt/1000))

        # Recolectar / Comer
        for r in list(self.world.resources):
            if self.pos.distance_to(r.position) < r.radius+4:
                self.inventory[r.kind] += r.amount
                if r.kind in ("food","crop"):
                    self.hunger = min(100, self.hunger + cfg["hunger_gain"])
                if r.kind == "meat":
                    self.hunger = min(100, self.hunger + cfg["meat_gain"])
                self.world.resources.remove(r)
                break

        # Cazar
        for a in list(self.world.animals):
            if self.pos.distance_to(a.pos) < 8:
                self.inventory["meat"] += 1
                self.hunger = min(100, self.hunger + cfg["meat_gain"])
                self.world.animals.remove(a)
                break

        # Investigación
        for tech in self.world.techs:
            if tech.name not in self.known_tech and tech.research(self):
                self.speed += cfg["tech_speed_bonus"]
                break

        # Plantar árbol
        if "Agriculture" in self.known_tech and self.agri_timer==0 and self.inventory["food"]>=5:
            # escoge baldosa vacía cerca de agua
            choices = [t for t in self.world.water_tiles]
            tile = random.choice(choices)
            self.world._create_tree(tile)
            self.inventory["food"] -= 5
            self.agri_timer = cfg["agriculture_interval"]

        # Crear granja
        if "Agriculture" in self.known_tech and self.farm_timer==0 and self.inventory["wood"]>=10:
            choices = [t for t in self.world.water_tiles]
            tile = random.choice(choices)
            self.world._create_farm(tile)
            self.inventory["wood"] -= 10
            self.farm_timer = cfg["farm_interval"]

        # Construir casa
        if self.house_timer==0 and self.inventory["wood"]>=10 and self.inventory["stone"]>=5:
            pos = (int(self.pos.x//cfg["tile_size"]), int(self.pos.y//cfg["tile_size"]))
            self.world._place_structure("House", pos)
            self.inventory["wood"]  -= 10
            self.inventory["stone"] -= 5
            self.house_timer = cfg["house_interval"]

        # Salud decae si hambre/sed 0
        if self.hunger==0 or self.thirst==0:
            self.health = max(0, self.health - cfg["health_decay_rate"] * dt)
        if self.health==0:
            self.alive = False
            return None

        # IA interna
        if self.advice_timer==0:
            self.advice_timer = cfg["advice_interval"]
            prompt = f"h={self.hunger:.1f},t={self.thirst:.1f},hl={self.health:.1f}. sugerencias:valor;..."
            advice = self.ai(prompt) or ""
            for part in advice.split(";"):
                if ":" in part:
                    k,v = part.split(":",1)
                    try: setattr(self,k.strip(), float(v))
                    except: pass

        # Movimiento
        target = self.think()
        if target:
            direction = (target - self.pos).normalize()
        else:
            angle     = random.uniform(0,2*math.pi)
            direction = Vector2(math.cos(angle), math.sin(angle))
        self.pos += direction * self.speed * (dt/1000)
        self.pos.x = max(0, min(self.world.width,  self.pos.x))
        self.pos.y = max(0, min(self.world.height, self.pos.y))

        # Reproducción
        if (self.hunger>=Tropel.REPRO_THRESHOLD
            and self.thirst>=Tropel.REPRO_THRESHOLD
            and self.repro_timer==0
            and len(self.world.tropeles)<cfg["max_tropeles"]):
            child = self.reproduce()
            self.repro_timer = Tropel.REPRO_COOLDOWN
            return child

        return None

    def reproduce(self):
        offset = Vector2(random.randint(-20,20), random.randint(-20,20))
        child  = Tropel(self.world, self.ai)
        child.pos        = self.pos + offset
        child.inventory  = self.inventory.copy()
        child.known_tech = set(self.known_tech)
        child.agri_timer = self.agri_timer
        child.farm_timer = self.farm_timer
        child.house_timer= self.house_timer
        child.structures = dict(self.structures)
        child.tools_code = dict(self.tools_code)
        self.hunger      = max(0, self.hunger - 20)
        self.thirst      = max(0, self.thirst - 20)
        return child
