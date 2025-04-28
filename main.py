# tropeles_game/main.py

import resource
import pygame

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
from core.camera        import Camera
from ui.minimap         import Minimap

# Limitar memoria virtual para prevenir OOM killer
LIMIT = 500 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))

def ask_questions():
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
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    pygame.display.set_caption("Tropeles Survival")
    font = pygame.font.SysFont(None, 24)

    world = World(SETTINGS)
    for _ in range(SETTINGS["initial_tropeles"]):
        world.add_tropel(Tropel(world))

    handler = InputHandler()
    menu    = Menu(screen, pygame.font.SysFont(None,36))
    cpanel  = ControlPanel(screen, font)
    ipanel  = InventoryPanel(screen, font)
    tpanel  = TechPanel(screen, world, font)
    camera  = Camera(world.width, world.height, screen_w, screen_h)
    minimap = Minimap(screen, world, camera)
    panels  = [cpanel, ipanel, tpanel]
    renderer= Renderer(screen, world, world.tropeles, panels, camera)

    running, in_menu = True, False
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60)

        # Procesar eventos de ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen_w, screen_h = event.w, event.h
                screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
                camera.view_w, camera.view_h = screen_w, screen_h
                minimap = Minimap(screen, world, camera)
            else:
                handler.process_event(event)

        # Pan con flechas
        keys = pygame.key.get_pressed()
        pan_sp = 300 * (dt/1000)
        if keys[pygame.K_LEFT]:  camera.move(-pan_sp, 0)
        if keys[pygame.K_RIGHT]: camera.move( pan_sp, 0)
        if keys[pygame.K_UP]:    camera.move(0, -pan_sp)
        if keys[pygame.K_DOWN]:  camera.move(0,  pan_sp)

        ok, click = handler.get_events()
        if not ok:
            break

        # Selección de tropel
        if click:
            sel = next(
                (t for t in world.tropeles if t.alive and t.pos.distance_to(click) < 6),
                None
            )
            cpanel.selected = sel
            ipanel.selected = sel
            tpanel.selected = sel

        cpanel.handle(click)
        tpanel.handle(click)
        minimap.handle(click)

        if in_menu:
            choice = menu.handle(click)
            menu.draw()
            if choice == "Restart":
                return main()
            elif choice == "Quit":
                break
        else:
            world.update(dt)
            if not world.tropeles:
                in_menu = True
            renderer.draw()
            minimap.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
