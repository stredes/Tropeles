import pygame

class TechPanel:
    """Muestra tecnologías y permite investigarlas."""
    def __init__(self, screen, world, font):
        self.screen  = screen
        self.world   = world
        self.font    = font
        self.width   = 200
        self.bg_color= (40,40,60)
        self.selected= None
        self.buttons= []  # lista de (tech, rect, can_research)

    def draw(self):
        panel = pygame.Rect(0,self.screen.get_height()-200,self.width,200)
        pygame.draw.rect(self.screen,self.bg_color,panel)
        title = self.font.render("Tecnologías",True,(255,255,255))
        self.screen.blit(title,(10,self.screen.get_height()-190))
        self.buttons.clear()
        y0 = self.screen.get_height()-160
        for tech in self.world.techs:
            color = (100,255,100) if tech.name in getattr(self.selected,"known_tech",()) else (255,255,255)
            txt = self.font.render(tech.name,True,color)
            self.screen.blit(txt,(10,y0))
            btn = pygame.Rect(120,y0,70,20)
            can = self.selected and tech.name not in self.selected.known_tech and all(
                self.selected.inventory.get(k,0)>=q for k,q in tech.requirements.items()
            )
            label = "▶" if can else "—"
            pygame.draw.rect(self.screen,(200,200,200),btn)
            lbl = self.font.render(label,True,(0,0,0))
            self.screen.blit(lbl,lbl.get_rect(center=btn.center))
            self.buttons.append((tech, btn, can))
            y0 += 30

    def handle(self, click):
        if self.selected and click: 
            for tech,btn,can in self.buttons:
                if can and btn.collidepoint(click):
                    tech.research(self.selected)
