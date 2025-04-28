class Technology:
    """
    Tecnología con requisitos y prerequisitos.
    - requirements: recurso→cantidad necesaria.
    - prereqs: lista de nombres de tecnologías previas.
    """
    def __init__(self, name: str, requirements: dict, prereqs: list[str]):
        self.name         = name
        self.requirements = requirements
        self.prereqs      = prereqs

    def can_research(self, tropel) -> bool:
        # Debe tener tecnologías previas
        if any(p not in tropel.known_tech for p in self.prereqs):
            return False
        # Debe tener recursos
        inv = tropel.inventory
        return all(inv.get(k, 0) >= q for k, q in self.requirements.items())

    def research(self, tropel) -> bool:
        """Consume recursos y registra la tecnología."""
        if not self.can_research(tropel):
            return False
        inv = tropel.inventory
        for k, q in self.requirements.items():
            inv[k] -= q
        tropel.known_tech.add(self.name)
        return True
