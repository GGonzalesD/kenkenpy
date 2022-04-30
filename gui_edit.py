import pygame
import pygame.locals as lcs
import events
from tools import draw_text

def ChangeData(surface:pygame.Surface, event:events.EventCtrl, back, grupo, rect:pygame.Rect):
    center = (surface.get_width()/2, surface.get_height()/2)
    cc = (0, 0)
    event.number = str(grupo['r'])

    rn = pygame.Rect(0, 0, 300, 60)
    btns = [pygame.Rect(0, 0, 60, 60) for _ in range(5)]
    r_ok =  pygame.Rect(0, 0, 150, 60)
    r_cn =  pygame.Rect(0, 0, 150, 60)
    op = grupo['op']
    operations = ['+', '-', 'x', '/', '.']
    mode = False
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)
    
    c_green = pygame.Color(0, 255, 0)
    c_green_g = pygame.Color(100, 200, 100)
    c_black = pygame.Color(0, 0, 0)
    c_blue_g = pygame.Color(80, 90, 110)
    c_white = pygame.Color(255, 255, 255)

    while True:
        surface.blit(back, (0, 0))
        mouse = pygame.mouse.get_pos()

        rn.bottom = center[1]
        rn.centerx = center[0]
        for i, r in enumerate(btns):
            r.topleft = (rn.left+i*60, rn.bottom)
        r_cn.topleft = ( rn.left, rn.bottom + 60 )
        r_ok.topleft = ( rn.centerx, rn.bottom + 60 )

        pygame.draw.rect(surface, c_green, rect, 4)
        pygame.draw.line(surface, c_green, rect.topleft, center, 4)

        pygame.draw.rect(surface, c_blue_g, rn)
        pygame.draw.rect(surface, c_black, rn, 2)
        draw_text(surface, rn.center, font, str(event.number)+"|", False)

        for i, r in enumerate(btns):
            if r.collidepoint(mouse):
                if event.mouse_down(1):
                    op = i
                pygame.draw.rect(surface, c_white, r)
            else:
                pygame.draw.rect(surface, c_green if op == i else c_blue_g, r)
            pygame.draw.rect(surface, c_black, r, 2)
            draw_text(surface, r.center, font, operations[i], False)
        
        if r_cn.collidepoint(mouse):
            pygame.draw.rect(surface, (255, 0, 0), r_cn)
            if event.mouse_down(1):
                mode = False
                break
        else:
            pygame.draw.rect(surface, (150, 0, 0), r_cn)
        pygame.draw.rect(surface, c_black, r_cn, 2)
        draw_text(surface, r_cn.center, font, "Cancelar", False)

        if r_ok.collidepoint(mouse):
            pygame.draw.rect(surface, (0, 255, 0), r_ok)
            if event.mouse_down(1):
                mode = True
                break
        else:
            pygame.draw.rect(surface, (0, 150, 0), r_ok)
        pygame.draw.rect(surface, c_black, r_ok, 2)
        draw_text(surface, r_ok.center, font, "Confirmar", False)

        event.update(pygame.event.get())

        if event.key_down(lcs.K_ESCAPE):
            mode = False
            break
        if event.key_down(lcs.K_RETURN):
            mode = True
            break
        if event.mouse_down(2):
            cc = (center[0]-mouse[0], center[1]-mouse[1])
        if event.mouse_press(2):
            center = (cc[0]+mouse[0], cc[1]+mouse[1])

        clock.tick(60)
        pygame.display.update()
    
    return (mode, op, event.number)