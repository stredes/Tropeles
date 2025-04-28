# tropeles_game/entities/animal.py

import random
import math
from pygame.math import Vector2

class Animal:
    """
    Animal que deambula, se reproduce pasivamente y puede ser cazado por los tropeles.
    - speed: velocidad de movimiento (px/s)
    - radius: radio de colisión para caza
    - repro_timer: tiempo restante (ms) hasta la próxima reproducción
    """
    def __init__(self, world):
        self.world       = world
        cfg              = world.config
        self.speed       = cfg["animal_speed"]
        self.radius      = 4
        # Generar posición aleatoria fuera del agua
        while True:
            x = random.uniform(0, world.width)
            y = random.uniform(0, world.height)
            tx, ty = int(x // world.tile_size), int(y // world.tile_size)
            if (tx, ty) not in world.water_tiles:
                self.pos = Vector2(x, y)
                break
        self.alive       = True
        # Tiempo aleatorio hasta reproducirse (entre 20s y 60s)
        self.repro_timer = random.randint(20000, 60000)

    def update(self, dt: float):
        """
        1) Deambula aleatoriamente
        2) Se reproduce pasivamente al expirar repro_timer
        """
        if not self.alive:
            return

        # 1) Movimiento aleatorio
        angle = random.uniform(0, 2 * math.pi)
        direction = Vector2(math.cos(angle), math.sin(angle))
        self.pos += direction * self.speed * (dt / 1000)

        # Mantener dentro de los límites del mundo
        self.pos.x = max(0, min(self.world.width,  self.pos.x))
        self.pos.y = max(0, min(self.world.height, self.pos.y))

        # 2) Reproducción pasiva
        self.repro_timer -= dt
        if self.repro_timer <= 0:
            # Reiniciar timer
            self.repro_timer = random.randint(20000, 60000)
            # Limitar población (opcional)
            max_animals = self.world.config.get("max_animals", 100)
            if len(self.world.animals) < max_animals:
                child = Animal(self.world)
                # Spawn cerca del padre
                offset = Vector2(random.randint(-20, 20), random.randint(-20, 20))
                child.pos = self.pos + offset
                self.world.animals.append(child)
