from pygame.math import Vector2

class Camera:
    """
    Gestiona el viewport dentro del mundo.
    world_w, world_h: dimensiones del mundo en px.
    view_w, view_h: dimensiones de la pantalla en px.
    """
    def __init__(self, world_w: int, world_h: int, view_w: int, view_h: int):
        self.world_w = world_w
        self.world_h = world_h
        self.view_w  = view_w
        self.view_h  = view_h
        self.x       = 0
        self.y       = 0

    def move(self, dx: float, dy: float):
        """Desplaza la cámara y la mantiene dentro de los límites."""
        self.x = max(0, min(self.world_w  - self.view_w,  self.x + dx))
        self.y = max(0, min(self.world_h - self.view_h, self.y + dy))

    def set_center(self, cx: float, cy: float):
        """Centra la cámara en (cx, cy), respetando los bordes."""
        self.x = max(0, min(self.world_w  - self.view_w,  cx - self.view_w // 2))
        self.y = max(0, min(self.world_h - self.view_h, cy - self.view_h // 2))

    def apply(self, pos: Vector2) -> Vector2:
        """Convierte una posición del mundo a coordenadas de pantalla."""
        return Vector2(pos.x - self.x, pos.y - self.y)
