class Resource:
    """
    Recurso en el mundo: food, wood, stone, metal.
    - amount: unidades recolectables.
    - ttl: tiempo de vida en ms, tras el cual desaparece.
    """
    RADII = {
        "food": 6,
        "wood": 8,
        "stone": 10,
        "metal": 12,
    }

    def __init__(self, kind: str, position: tuple, amount: int = 1, ttl: int | None = None):
        self.kind     = kind
        self.position = position  # (x, y)
        self.amount   = amount
        self.radius   = Resource.RADII.get(kind, 6)
        self.ttl      = ttl       # en ms; None => infinita

    def update(self, dt):
        """Decrementa ttl y retorna False si expira."""
        if self.ttl is None:
            return True
        self.ttl -= dt
        return self.ttl > 0
    