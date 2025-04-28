import pygame
from pygame.math import Vector2

class Minimap:
    """
    Mapa en miniatura interactivo.
    Al hacer clic, reposiciona la cámara.
    """
    def __init__(self, screen: pygame.Surface, world, camera, width: int = 200, margin: int = 10):
        self.screen  = screen
        self.world   = world
        self.camera  = camera
        self.width   = width
        self.margin  = margin
        # Calcular alto manteniendo proporción del mundo
        self.height  = int(world.height * (width / world.width))
        # Rectángulo donde se dibuja el minimapa
        self.rect    = pygame.Rect(
            screen.get_width() - width - margin,
            screen.get_height() - self.height - margin,
            width, self.height
        )

    def draw(self):
        surf = pygame.Surface((self.width, self.height))
        surf.fill((30, 30, 30))

        sx = self.width  / self.world.width
        sy = self.height / self.world.height

        # Dibujar agua
        for (i, j) in self.world.water_tiles:
            x = i * self.world.tile_size * sx
            y = j * self.world.tile_size * sy
            size = self.world.tile_size * sx
            pygame.draw.rect(surf, (0, 191, 255), (x, y, size, size))

        # Dibujar árboles
        for (i, j) in self.world.trees:
            x = (i * self.world.tile_size + self.world.tile_size / 2) * sx
            y = (j * self.world.tile_size + self.world.tile_size / 2) * sy
            pygame.draw.circle(surf, (34, 139, 34), (int(x), int(y)), 2)

        # Dibujar tropeles
        for t in self.world.tropeles:
            if t.alive:
                x = t.pos.x * sx
                y = t.pos.y * sy
                pygame.draw.circle(surf, (255, 215, 0), (int(x), int(y)), 2)

        # Dibujar rectángulo de la vista actual
        vx = self.camera.x * sx
        vy = self.camera.y * sy
        vw = self.camera.view_w * sx
        vh = self.camera.view_h * sy
        pygame.draw.rect(surf, (255, 255, 255), (vx, vy, vw, vh), 1)

        # Pegar el minimapa en pantalla
        self.screen.blit(surf, (self.rect.x, self.rect.y))

    def handle(self, click):
        """Si se hace clic dentro del minimapa, centra la cámara en ese punto."""
        if not click:
            return
        if self.rect.collidepoint(click):
            mx = click[0] - self.rect.x
            my = click[1] - self.rect.y
            wx = mx * self.world.width  / self.width
            wy = my * self.world.height / self.height
            self.camera.set_center(wx, wy)
