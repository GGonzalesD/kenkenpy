import pygame
import pygame.locals as lcs
import events, glob
from tools import draw_label, draw_boton_if
from gui_msg import message_box_warning, message_box_bool

def GuiLoad(surface:pygame.Surface, event:events.EventCtrl, back, grupos):
    event.reset()

    center = (surface.get_width()/2, surface.get_height()/2)
    font = pygame.font.SysFont('Arial', 20)
    clock = pygame.time.Clock()

    r = pygame.Rect(0, 0, 400, 80)

    files = []
    for f in glob.glob("save/*.json"):
        f = f.replace("\\", "/")
        files.append(f.split("/")[-1])

    while True:
        surface.blit(back, (0, 0))
        mouse = pygame.mouse.get_pos()
        event.update(pygame.event.get())

        t = event.text
        r.center = center
        t = t.replace(" ", "_")
        draw_label(surface, r, font, t+"|.json", (150, 150, 150))

        acc = r.bottom
        for fname in files:
            if t in fname:
                rx = pygame.Rect(r)
                rx.top = acc + 2
                acc += r.height
                if draw_boton_if(surface, event, rx, mouse, font, fname, (100, 100, 255), (100, 100, 150)):
                    return fname

        if event.key_down(lcs.K_ESCAPE):
            break

        clock.tick(60)
        pygame.display.update()
    return None