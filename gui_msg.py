import pygame
import pygame.locals as lcs
import events
from tools import draw_label, draw_boton_if

def message_box_warning(surface:pygame.Surface, event:events.EventCtrl, back, text):
    center = (surface.get_width()/2, surface.get_height()/2)
    font = pygame.font.SysFont('Arial', 20)
    clock = pygame.time.Clock()

    c_yellow = pygame.Color(255, 150, 0)
    c_yelow_d = pygame.Color(150, 150, 0)

    r = pygame.Rect(0, 0, 300, 80)
    r_ok = pygame.Rect(0, 0, 300, 80)

    while True:
        surface.blit(back, (0, 0))
        mouse = pygame.mouse.get_pos()
        event.update(pygame.event.get())

        r.centerx = center[0]
        r.bottom = center[1]
        r_ok.topleft = r.bottomleft

        draw_label(surface, r, font, text, (190, 190, 150))
        if draw_boton_if(surface, event, r_ok, mouse, font, "OK", c_yellow, c_yelow_d):
            break

        clock.tick(60)
        pygame.display.update()

def message_box_bool(surface:pygame.Surface, event:events.EventCtrl, back, text):
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

    while True:
        surface.blit(back, (0, 0))
        mouse = pygame.mouse.get_pos()
        event.update(pygame.event.get())

        r.centerx = center[0]
        r.bottom = center[1]
        r_no.topleft = r.bottomleft
        r_yes.topleft = r_no.topright

        draw_label(surface, r, font, text, (150, 150, 150))
        if draw_boton_if(surface, event, r_no, mouse, font, "NO", c_red, c_red_d):
            return False
        if draw_boton_if(surface, event, r_yes, mouse, font, "SI", c_green, c_green_d):
            return True

        if event.key_down(lcs.K_ESCAPE):
            break

        clock.tick(60)
        pygame.display.update()
    return False