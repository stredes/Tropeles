import pygame

class InputHandler:
    """Procesa eventos y devuelve click pos o QUIT."""
    def get_events(self):
        click = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                click = event.pos
        return True, click
