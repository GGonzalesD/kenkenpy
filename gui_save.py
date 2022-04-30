import pygame
import pygame.locals as lcs
import events, glob
from tools import draw_label, draw_boton_if
from gui_msg import message_box_warning, message_box_bool


def GuiSave(surface:pygame.Surface, event:events.EventCtrl, back, grupos, mainfname):
    event.reset()
    if mainfname != None:
        event.text = mainfname.split(".")[0]

    center = (surface.get_width()/2, surface.get_height()/2)
    font = pygame.font.SysFont('Arial', 20)
    clock = pygame.time.Clock()

    c_red = pygame.Color(255, 0, 0)
    c_red_d = pygame.Color(150, 0, 0)

    c_green = pygame.Color(0, 255, 0)
    c_green_d = pygame.Color(0, 150, 0)

    r = pygame.Rect(0, 0, 400, 80)
    r_no = pygame.Rect(0, 0, 200, 80)
    r_yes = pygame.Rect(0, 0, 200, 80)

    files = []
    for f in glob.glob("save/*.json"):
        f = f.replace("\\", "/")
        files.append(f.split("/")[-1])

    while True:
        surface.blit(back, (0, 0))
        mouse = pygame.mouse.get_pos()
        event.update(pygame.event.get())

        r.center = center
        r_no.topleft = r.bottomleft
        r_yes.topleft = r_no.topright

        t = event.text
        t = t.replace(" ", "_")
        draw_label(surface, r, font, t+"|.json", (150, 150, 150))

        if draw_boton_if(surface, event, r_no, mouse, font, "NO", c_red, c_red_d):
            return None
        if draw_boton_if(surface, event, r_yes, mouse, font, "SI", c_green, c_green_d):
            if len(t) == 0:
                message_box_warning(surface, event, back, "Nombre Invalido")
            elif t+".json" in files:
                if message_box_bool(surface, event, back, f"Sobrecribir '{t+'.json'}'"):
                    return t+".json"
            else:
                return t+".json"

        if event.key_down(lcs.K_ESCAPE):
            break

        clock.tick(60)
        pygame.display.update()
    return None