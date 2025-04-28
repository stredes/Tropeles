import pygame

class Menu:
    """Pantalla de Game Over con Restart/Quit."""
    def __init__(self, screen, font):
        self.screen  = screen
        self.font    = font
        w,h          = screen.get_size()
        self.buttons = {
            "Restart": pygame.Rect(w//2-80,h//2-20,160,40),
            "Quit":    pygame.Rect(w//2-80,h//2+40,160,40),
        }

    def draw(self):
        self.screen.fill((10,10,10))
        t = self.font.render("Game Over",True,(255,255,255))
        self.screen.blit(t,t.get_rect(center=(self.screen.get_width()//2,100)))
        for txt,btn in self.buttons.items():
            pygame.draw.rect(self.screen,(200,200,200),btn)
            lbl = self.font.render(txt,True,(0,0,0))
            self.screen.blit(lbl,lbl.get_rect(center=btn.center))
        pygame.display.flip()

    def handle(self, click):
        if click:
            for txt,btn in self.buttons.items():
                if btn.collidepoint(click):
                    return txt
        return None
