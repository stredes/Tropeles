import pygame

class Renderer:
    """Dibuja mundo, árboles, recursos persistentes, tropeles y UI."""
    def __init__(self, screen, world, tropeles, panels):
        self.screen   = screen
        self.world    = world
        self.tropeles = tropeles
        self.panels   = panels

    def draw(self):
        ts = self.world.tile_size
        self.screen.fill((34,139,34))  # césped

        # Agua
        for (i,j) in self.world.water_tiles:
            pygame.draw.rect(self.screen, (0,191,255),(i*ts,j*ts,ts,ts))

        # Árboles
        for (i,j) in self.world.trees:
            x,y = i*ts+ts//2, j*ts+ts//2
            pygame.draw.rect(self.screen,(139,69,19),(x-3,y,6,ts//2))
            pygame.draw.circle(self.screen,(34,139,34),(x,y),ts//2)

        # Recursos (solo los que no expiraron)
        for r in self.world.resources:
            color = {
                "food": (255,0,0),
                "wood": (160,82,45),
                "stone":(128,128,128),
                "metal":(192,192,192)
            }[r.kind]
            pygame.draw.circle(
                self.screen,
                color,
                (int(r.position[0]), int(r.position[1])),
                r.radius
            )

        # Tropeles
        for t in self.tropeles:
            if not t.alive: continue
            px,py = int(t.pos.x), int(t.pos.y)

            # Salud
            bw,bh = 12,3
            hr = t.health / 100
            pygame.draw.rect(self.screen,(255,0,0),(px-bw//2,py-14,bw,bh))
            pygame.draw.rect(self.screen,(0,255,0),(px-bw//2,py-14,int(bw*hr),bh))

            # Hambre
            pygame.draw.rect(self.screen,(255,0,0),(px-6,py-10,12,2))
            pygame.draw.rect(self.screen,(0,255,0),(px-6,py-10,int(12*t.hunger/100),2))

            # Sed
            pygame.draw.rect(self.screen,(0,0,0),(px-6,py-7,12,2))
            pygame.draw.rect(self.screen,(0,191,255),(px-6,py-7,int(12*t.thirst/100),2))

            # Cuerpo
            pygame.draw.circle(self.screen,(255,215,0),(px,py),4)

        # Paneles UI
        for panel in self.panels:
            panel.draw()

        pygame.display.flip()
import pygame

class Renderer:
    """Dibuja mundo, árboles, recursos persistentes, tropeles y UI."""
    def __init__(self, screen, world, tropeles, panels):
        self.screen   = screen
        self.world    = world
        self.tropeles = tropeles
        self.panels   = panels

    def draw(self):
        ts = self.world.tile_size
        self.screen.fill((34,139,34))  # césped

        # Agua
        for (i,j) in self.world.water_tiles:
            pygame.draw.rect(self.screen, (0,191,255),(i*ts,j*ts,ts,ts))

        # Árboles
        for (i,j) in self.world.trees:
            x,y = i*ts+ts//2, j*ts+ts//2
            pygame.draw.rect(self.screen,(139,69,19),(x-3,y,6,ts//2))
            pygame.draw.circle(self.screen,(34,139,34),(x,y),ts//2)

        # Recursos (solo los que no expiraron)
        for r in self.world.resources:
            color = {
                "food": (255,0,0),
                "wood": (160,82,45),
                "stone":(128,128,128),
                "metal":(192,192,192)
            }[r.kind]
            pygame.draw.circle(
                self.screen,
                color,
                (int(r.position[0]), int(r.position[1])),
                r.radius
            )

        # Tropeles
        for t in self.tropeles:
            if not t.alive: continue
            px,py = int(t.pos.x), int(t.pos.y)

            # Salud
            bw,bh = 12,3
            hr = t.health / 100
            pygame.draw.rect(self.screen,(255,0,0),(px-bw//2,py-14,bw,bh))
            pygame.draw.rect(self.screen,(0,255,0),(px-bw//2,py-14,int(bw*hr),bh))

            # Hambre
            pygame.draw.rect(self.screen,(255,0,0),(px-6,py-10,12,2))
            pygame.draw.rect(self.screen,(0,255,0),(px-6,py-10,int(12*t.hunger/100),2))

            # Sed
            pygame.draw.rect(self.screen,(0,0,0),(px-6,py-7,12,2))
            pygame.draw.rect(self.screen,(0,191,255),(px-6,py-7,int(12*t.thirst/100),2))

            # Cuerpo
            pygame.draw.circle(self.screen,(255,215,0),(px,py),4)

        # Paneles UI
        for panel in self.panels:
            panel.draw()

        pygame.display.flip()
