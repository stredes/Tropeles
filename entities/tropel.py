import math
import random
from pygame.math import Vector2
from ai.ollama_client import query
from entities.resource import Resource

class Tropel:
    """
    Tropel: IA, inventario, recolección, investigación, construcción de estructuras
    y generación de código para nuevas herramientas.
    """
    REPRO_THRESHOLD = 95

    def __init__(self, world, ai_client=query):
        self.world        = world
        self.ai           = ai_client
        cfg                = world.config

        cx, cy             = world.width // 2, world.height // 2
        self.pos          = Vector2(cx, cy)
        self.speed        = cfg["tropel_speed"]
        self.hunger       = 100.0
        self.thirst       = 100.0
        self.health       = 100.0
        self.alive        = True
        self.comm_radius  = cfg["communication_radius"]

        # Inventario y tecnologías
        self.inventory    = {k: 0 for k in cfg["resource_spawn_intervals"].keys()}
        self.known_tech   = set()

        # Estructuras construidas y código de herramientas
        self.structures   = {}   # e.g. {"House": 1}
        self.tools_code   = {}   # e.g. {"House": "<class House: ...>"}

        # Temporizador para IA interna
        self.advice_timer = 0

    def think(self):
        """
        Decide objetivo: beber, comer, recolectar, investigar o construir.
        Devuelve Vector2 destino o None para deambular.
        """
        cfg = self.world.config

        # 1) Beber si sed > hambre
        if self.thirst < self.hunger and self.world.water_tiles:
            return self._find_nearest_water()

        # 2) Comer si hambre crítica sin comida
        if self.hunger < 50 and self.inventory["food"] == 0:
            foods = [r for r in self.world.resources if r.kind == "food"]
            if foods:
                return self._find_nearest_resource(foods)

        # 3) Recolectar recursos faltantes
        for kind in ("wood", "stone", "metal"):
            if kind not in self.known_tech and self.inventory[kind] < 5:
                res = [r for r in self.world.resources if r.kind == kind]
                if res:
                    return self._find_nearest_resource(res)

        # 4) Investigar tecnología pendiente
        for tech in self.world.techs:
            if tech.name not in self.known_tech:
                if all(self.inventory.get(k, 0) >= q for k, q in tech.requirements.items()):
                    return None  # quedarse para investigar

        # 5) Construir estructura si posible
        for name, reqs in cfg.get("structures", {}).items():
            if all(self.inventory.get(k, 0) >= q for k, q in reqs.items()):
                return None  # pausa para construir

        # 6) Deambular
        return None

    def _find_nearest_water(self):
        best = min(
            self.world.water_tiles,
            key=lambda t: (self.pos.x/self.world.tile_size - t[0])**2
                        + (self.pos.y/self.world.tile_size - t[1])**2
        )
        x = best[0]*self.world.tile_size + self.world.tile_size//2
        y = best[1]*self.world.tile_size + self.world.tile_size//2
        return Vector2(x, y)

    def _find_nearest_resource(self, resources):
        res = min(resources, key=lambda r: self.pos.distance_to(r.position))
        return Vector2(res.position)

    def update(self, dt):
        """
        Actualiza hambre, sed, salud, recolección, investigación,
        construcción, IA interna, movimiento y reproducción.
        """
        if not self.alive:
            return None
        cfg = self.world.config

        # 1) Hambre y sed
        self.hunger -= cfg["hunger_rate"] * dt
        self.thirst -= cfg["thirst_rate"] * dt

        # 2) Beber si sobre baldosa de agua
        tx = int(self.pos.x // cfg["tile_size"])
        ty = int(self.pos.y // cfg["tile_size"])
        if (tx, ty) in self.world.water_tiles:
            self.thirst = min(100.0, self.thirst + cfg["thirst_gain"] * (dt/1000))

        # 3) Recolectar recursos
        for r in list(self.world.resources):
            if self.pos.distance_to(r.position) < r.radius + 4:
                self.inventory[r.kind] += r.amount
                if r.kind == "food":
                    self.hunger = min(100.0, self.hunger + cfg["hunger_gain"])
                self.world.resources.remove(r)
                break

        # 4) Investigar tecnología disponible
        for tech in self.world.techs:
            if tech.name not in self.known_tech and tech.research(self):
                self.speed += cfg.get("tech_speed_bonus", 10)
                break

        # 5) Construir estructura si posibles requisitos
        for name, reqs in cfg.get("structures", {}).items():
            if all(self.inventory.get(k, 0) >= q for k, q in reqs.items()):
                self._build_structure(name, reqs)
                break

        # 6) Salud
        if self.hunger <= 0 or self.thirst <= 0:
            self.health -= cfg["health_decay_rate"] * dt
        if self.health <= 0:
            self.alive = False
            return None

        # 7) IA interna cada intervalo
        self.advice_timer += dt
        if self.advice_timer >= cfg.get("advice_interval"):
            self.advice_timer %= cfg.get("advice_interval")
            prompt = f"h={self.hunger:.1f},t={self.thirst:.1f},hl={self.health:.1f}. sugerencias clave:valor;..."
            advice = self.ai(prompt) or ""
            for part in advice.split(";"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    try:
                        setattr(self, k.strip(), float(v))
                    except ValueError:
                        pass

        # 8) Movimiento
        target = self.think()
        if target:
            direction = (target - self.pos).normalize()
        else:
            angle = random.uniform(0, 2*math.pi)
            direction = Vector2(math.cos(angle), math.sin(angle))
        self.pos += direction * self.speed * (dt/1000)
        self.pos.x = max(0, min(self.world.width, self.pos.x))
        self.pos.y = max(0, min(self.world.height, self.pos.y))

        # 9) Reproducción con límite
        if (self.hunger >= Tropel.REPRO_THRESHOLD
            and self.thirst >= Tropel.REPRO_THRESHOLD
            and len(self.world.tropeles) < cfg.get("max_tropeles")):
            return self.reproduce()

        return None

    def _build_structure(self, name, requirements):
        """
        Consume recursos, registra la estructura, genera código vía IA
        y lo almacena en self.tools_code[name].
        """
        # Restar recursos
        for k, q in requirements.items():
            self.inventory[k] -= q
        # Contar estructura
        self.structures[name] = self.structures.get(name, 0) + 1

        # Generar código para herramienta/estructura
        prompt = (
            f"Genera la definición en Python de una clase '{name}' que "
            "implemente la lógica de construcción y uso de esta estructura en el juego. "
            "Devuelve solo la clase con sus métodos."
        )
        code = self.ai(prompt) or ""
        self.tools_code[name] = code

        # Ejecutar dinámicamente el código generado
        try:
            # namespace local para exec
            local_ns = {}
            exec(code, globals(), local_ns)
            # opcional: registrar la clase en world.tools
            if hasattr(self.world, "tools"):
                self.world.tools[name] = local_ns.get(name)
        except Exception:
            pass

    def reproduce(self):
        """Genera un hijo transfiriendo inventario, tecnología y estructuras."""
        offset = Vector2(random.randint(-20, 20), random.randint(-20, 20))
        child = Tropel(self.world, self.ai)
        child.pos        = self.pos + offset
        child.inventory  = self.inventory.copy()
        child.known_tech = set(self.known_tech)
        child.structures = dict(self.structures)
        child.tools_code = dict(self.tools_code)
        # Reducir bienestar del padre
        self.hunger = max(0.0, self.hunger - 20)
        self.thirst = max(0.0, self.thirst - 20)
        return child
