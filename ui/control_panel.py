import pygame

class ControlPanel:
    """Muestra stats de tropel y botones Feed/Drink."""
    def __init__(self, screen, font):
        self.screen    = screen
        self.font      = font
        self.width     = 200
        self.bg_color  = (50,50,50)
        self.buttons   = {
            "Feed":  pygame.Rect(self.screen.get_width()-180,100,160,30),
            "Drink": pygame.Rect(self.screen.get_width()-180,140,160,30),
        }
        self.selected = None

    def draw(self):
        panel = pygame.Rect(self.screen.get_width()-self.width,0,self.width,self.screen.get_height())
        pygame.draw.rect(self.screen,self.bg_color,panel)
        title = self.font.render("Control Tropel",True,(255,255,255))
        self.screen.blit(title,(panel.x+10,10))
        if self.selected:
            stats = [
                f"Hambre: {int(self.selected.hunger)}",
                f"Sed:     {int(self.selected.thirst)}",
                f"Salud:   {int(self.selected.health)}",
            ]
            for i, line in enumerate(stats):
                txt = self.font.render(line,True,(255,255,255))
                self.screen.blit(txt,(panel.x+10,40+i*20))
        for action, btn in self.buttons.items():
            pygame.draw.rect(self.screen,(200,200,200),btn)
            lbl = self.font.render(action,True,(0,0,0))
            self.screen.blit(lbl,lbl.get_rect(center=btn.center))

    def handle(self, click):
        if self.selected and click:
            for action,btn in self.buttons.items():
                if btn.collidepoint(click):
                    if action=="Feed":
                        self.selected.hunger = min(100,self.selected.hunger+20)
                    elif action=="Drink":
                        self.selected.thirst = min(100,self.selected.thirst+30)
