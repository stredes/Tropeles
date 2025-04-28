import pygame

class InventoryPanel:
    """Muestra inventario del tropel seleccionado."""
    def __init__(self, screen, font):
        self.screen   = screen
        self.font     = font
        self.width    = 200
        self.bg_color = (30,30,30)
        self.selected = None

    def draw(self):
        panel = pygame.Rect(0,0,self.width,self.screen.get_height())
        pygame.draw.rect(self.screen,self.bg_color,panel)
        title = self.font.render("Inventario",True,(255,255,255))
        self.screen.blit(title,(10,10))
        if self.selected:
            for i,(k,v) in enumerate(self.selected.inventory.items()):
                txt = self.font.render(f"{k}: {v}",True,(200,200,200))
                self.screen.blit(txt,(10,40+i*20))
