# tropeles_game/main.py

import resource
import pygame
import random

from utils.persistence import Persistence
from configs.settings   import SETTINGS
from core.world         import World
from entities.tropel    import Tropel
from ui.renderer        import Renderer
from ui.input_handler   import InputHandler
from ui.menu            import Menu
from ui.control_panel   import ControlPanel
from ui.inventory_panel import InventoryPanel
from ui.tech_panel      import TechPanel

# --- Limitar memoria virtual para prevenir OOM killer ---
LIMIT = 500 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))

def ask_questions():
    """Pregunta al usuario al inicio y almacena respuestas en JSON."""
    p = Persistence("questions.json")
    qs = [
        "¿Cómo quieres llamar a tu mundo?",
        "¿Nivel de desafío? (fácil/medio/difícil)",
        "¿Objetivo final para los tropeles?"
    ]
    for q in qs:
        if not p.has_answer(q):
            ans = input(q + " ")
            p.store(q, ans)
    print("Bienvenido al mundo:", p.get(qs[0]))

def main():
    ask_questions()

    pygame.init()
    screen = pygame.display.set_mode(SETTINGS["world_size"], vsync=1)
    pygame.display.set_caption("Tropeles Survival")
    font   = pygame.font.SysFont(None, 24)

    # Crear mundo y tropeles
    world = World(SETTINGS)
    for _ in range(SETTINGS["initial_tropeles"]):
        world.add_tropel(Tropel(world))

    handler = InputHandler()
    menu    = Menu(screen, pygame.font.SysFont(None,36))
    cpanel  = ControlPanel(screen, font)
    ipanel  = InventoryPanel(screen, font)
    tpanel  = TechPanel(screen, world, font)
    panels  = [cpanel, ipanel, tpanel]

    renderer = Renderer(screen, world, world.tropeles, panels)

    selected   = None
    running    = True
    in_menu    = False
    clock      = pygame.time.Clock()

    while running:
        dt, click = clock.tick(60), None
        ok, click = handler.get_events()
        if not ok:
            break

        # Selección de tropel si clicas sobre uno
        if click:
            sel = next(
                (t for t in world.tropeles
                 if t.alive and t.pos.distance_to(click) < 6),
                None
            )
            selected           = sel
            cpanel.selected    = sel
            ipanel.selected    = sel
            tpanel.selected    = sel

        # Paneles reaccionan al clic
        cpanel.handle(click)
        tpanel.handle(click)

        if in_menu:
            choice = menu.handle(click)
            menu.draw()
            if choice == "Restart":
                return main()
            elif choice == "Quit":
                break
        else:
            # Actualiza lógica de mundo y tropeles
            world.update(dt)

            # Si ya no quedan tropeles, pasa a menú
            if not world.tropeles:
                in_menu = True

            # Dibuja todo
            renderer.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
